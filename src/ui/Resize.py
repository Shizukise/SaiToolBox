from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFileDialog, QMessageBox, QScrollArea, QDialog
)
from PySide6.QtCore import Qt
from src.utils.ListItem import ListItem
from src.utils.ConfirmationResize import ResizeConfirmationDialog, ResizeOrientationDialog
from src.controllers.FIleOperatorResize import FileOperator
import os, platform, subprocess

class ResizePdf(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)  # Set the fixed window size
        self.setWindowTitle("PDF RESIZE")  # Set the window title
        self.on_hold = []  # List to hold files waiting for action
        self.names = {}  # Dictionary for storing file names and their corresponding ListItems
        self.currently_selected = {}  # Dictionary for keeping track of selected files
        self.currently_selected_label = f"Actuellement {len(self.currently_selected)} fichiers sélectionnés"  # Label to display the number of selected files

        # Create the central widget for the window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        """Operator class that holds the methods for pdf operations"""
        self.operator = FileOperator(parent=central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins for full-width design
        main_layout.setSpacing(0)

        # Header Section
        header = QLabel("PDF RESIZE")
        header.setStyleSheet("""
            background-color: #1E1E1E;
            color: #FF6F61;
            font-size: 28px;
            font-weight: bold;
            padding: 15px;
            border-bottom: 3px solid #FF6F61;
        """)
        header.setAlignment(Qt.AlignCenter)  # Center the header text
        header.setFixedHeight(70)  # Set fixed height for the header
        main_layout.addWidget(header)

        # Content layout (horizontal layout)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)

        # Sidebar (left side of the layout)
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            background-color: #292929;
            border-right: 3px solid #FF6F61;
        """)
        sidebar.setFixedWidth(300)  # Set fixed width for the sidebar

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        # Upload Button
        upload_bl_button = self.create_button("Upload", background="#FF6F61")
        upload_bl_button.clicked.connect(self.upload_files_and_render)
        sidebar_layout.addWidget(upload_bl_button)

        # Scrollable area for displaying file names
        self.file_names_scroll_area = QScrollArea()
        self.file_names_scroll_area.setWidgetResizable(True)
        self.file_names_widget = QWidget()
        self.file_names_layout = QVBoxLayout(self.file_names_widget)
        self.file_names_scroll_area.setWidget(self.file_names_widget)
        sidebar_layout.addWidget(self.file_names_scroll_area)

        content_layout.addWidget(sidebar)  # Add sidebar to the content layout

        # Main Area (right side of the layout)
        main_area = QFrame()
        main_area.setStyleSheet("""
            background-color: #1E1E1E;
        """)
        main_area_layout = QVBoxLayout(main_area)
        main_area_layout.setContentsMargins(30, 30, 30, 30)
        main_area_layout.setSpacing(20)

        # Description Label
        description_label = QLabel("Sélectionnez un format pour redimensionner votre PDF")
        description_label.setStyleSheet("""
            color: #D3D3D3;
            font-size: 16px;
            font-weight: bold;
        """)
        description_label.setAlignment(Qt.AlignCenter)
        main_area_layout.addWidget(description_label)

        # Selected Files Label
        self.files_selected_label = QLabel(self.currently_selected_label)
        self.files_selected_label.setStyleSheet("""
            color: #A9A9A9;
            font-size: 14px;
        """)
        self.files_selected_label.setAlignment(Qt.AlignCenter)
        main_area_layout.addWidget(self.files_selected_label)

        # Button Layout for Predefined Formats
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        formats = ["A4", "A3", "A2", "A1", "A0"]
        for fmt in formats:
            button = self.create_button(fmt)
            button.clicked.connect(lambda checked, f=fmt: self.ask_for_resizeA(f))
            button_layout.addWidget(button)

        main_area_layout.addLayout(button_layout)

        # Custom Size Buttons Layout
        custom_button_layout = QHBoxLayout()
        custom_button_layout.setSpacing(10)

        Resize300x500Button = self.create_button("300x500")
        Resize300x500Button.clicked.connect(lambda: self.ask_for_resizeA("300x500"))  #Different method as this works a bit differently
        custom_button_layout.addWidget(Resize300x500Button)

        CustomSizeButton = self.create_button("Custom")
        CustomSizeButton.clicked.connect(lambda: self.ask_for_resizeB())
        custom_button_layout.addWidget(CustomSizeButton)

        main_area_layout.addLayout(custom_button_layout)

        # Open Folder Button (to open the folder where resized PDFs are stored)
        open_folder_button = self.create_button("Download", background="#FF6F61")
        open_folder_button.clicked.connect(lambda: self.open_download_folder())
        main_area_layout.addWidget(open_folder_button, alignment=Qt.AlignCenter)

        content_layout.addWidget(main_area)  # Add main area to the content layout
        main_layout.addLayout(content_layout)  # Add content layout to the main layout

        # Footer
        footer = QLabel("© 2024 SaiToolBox | All Rights Reserved")
        footer.setStyleSheet("""
            background-color: #292929;
            color: #D3D3D3;
            font-size: 14px;
            padding: 10px;
            border-top: 3px solid #FF6F61;
        """)
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(50)
        main_layout.addWidget(footer)

        # Load initial files
        self.operator.folder_reader(self.on_hold)
        self.render_on_hold(self.file_names_layout)

        # Center the window
        self.center_window()

    def create_button(self, text, background="#3E3E3E", color="#FFFFFF"):
        """Creates a styled button"""
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {background};
                color: {color};
                font-size: 14px;
                padding: 10px 15px;
                border-radius: 8px;
                border: 2px solid #FF6F61;
            }}
            QPushButton:hover {{
                background-color: #FF6F61;
                color: #1E1E1E;
            }}
        """)
        button.setFixedSize(120, 40)
        return button
    

    def upload_files_and_render(self):
        """Handles the uploading of files and renders them in the UI"""
        self.operator.upload_files(self)
        self.operator.folder_reader(self.on_hold)
        self.render_on_hold(self.file_names_layout)

    def render_on_hold(self, parent):
        """Renders the list of files on hold into the UI"""
        # Clear existing widgets
        for i in reversed(range(parent.count())):
            widget = parent.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add new widgets for each file
        for file_name in reversed(self.on_hold):  # Iterate over items in self.on_hold
            name = ListItem(text=file_name)
            self.names[name.name] = name
            parent.addWidget(name)
            name.selection_changed.connect(self.handle_selection_changed)
        self.files_selected_label.setText(f"Actuellement {len(self.currently_selected)} fichiers sélectionnés")

    def handle_selection_changed(self, file_name, selected):
        """Updates the selected files dictionary and updates the label"""
        if selected:
            self.currently_selected[file_name] = True
        else:
            if file_name in self.currently_selected:
                del self.currently_selected[file_name]
        self.files_selected_label.setText(f"Actuellement {len(self.currently_selected)} fichiers sélectionnés")

    def ask_for_resizeA(self, format):
        """Prompts the user for confirmation before resizing the selected files
           Method for resize method A"""
        
        if len(self.currently_selected) == 0:
            QMessageBox.warning(self, "Aucun fichier sélectionné", "Veuillez sélectionner des fichiers à redimensionner.")
        else:
            # Create and show a custom confirmation dialog
            dialog = ResizeConfirmationDialog(format, self)
            result = dialog.exec_()

            # Check dialog result
            if result == QDialog.Accepted:  # User clicked 'Yes'
                self.operator.resizeFilesA(format, self.currently_selected)
                on_hold_new = []
                for i in self.on_hold:
                    if i not in self.currently_selected.keys():
                        on_hold_new.append(i)
                    else:
                        del self.currently_selected[i] 
                self.on_hold = on_hold_new
                self.render_on_hold(self.file_names_layout)
                QMessageBox.information(self, "Redimensionnement réussi", f"Les fichiers ont été redimensionnés en {format}.")
            else:  # User clicked 'No'
                print("User selected 'No' or canceled.")

    def ask_for_resizeB(self):
        """Prompts the user for confirmation before resizing the selected files
           Method for resize method B (Custom)"""
        horizontal = False
        if len(self.currently_selected) == 0:
            QMessageBox.warning(self, "Aucun fichier sélectionné", "Veuillez sélectionner des fichiers à redimensionner.")
        else:
            # Create and show a custom confirmation dialog
            dialog_orientation = ResizeOrientationDialog(self)
            dialog = ResizeConfirmationDialog("Custom", self)
            result = dialog.exec_()
            orientation, custom_format = dialog_orientation.exec_()
            # Check dialog result
            if result == QDialog.Accepted:  # User clicked 'Yes'
                self.operator.ResizeFilesB(self.currently_selected,orientation,custom_format)
                on_hold_new = []
                for i in self.on_hold:
                    if i not in self.currently_selected.keys():
                        on_hold_new.append(i)
                    else:
                        del self.currently_selected[i] 
                self.on_hold = on_hold_new
                self.render_on_hold(self.file_names_layout)
                QMessageBox.information(self, "Redimensionnement réussi", f"Les fichiers ont été redimensionnés.")
            else:  # User clicked 'No'
                print("User selected 'No' or canceled.")

    def show_custom_size_dialog(self):
        """Handles custom size dialog"""
        pass

    def open_download_folder(self):
        """Opens the folder containing the resized PDFs"""
        folder_path = '/home/galopin/Wa Its/src/data/PostResize' 
        if platform.system() == 'Windows':
            os.startfile(folder_path)
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', folder_path])
        else:
            print("Unsupported OS")

    def center_window(self):
        """Centers the window on the screen when it is opened"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_width = self.width()
        window_height = self.height()
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.move(x, y)
