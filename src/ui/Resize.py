import os, shutil
import fitz
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFileDialog, QMessageBox, QScrollArea, QVBoxLayout,QDialog
)
from src.utils.ListItem import ListItem
from PySide6.QtCore import Qt, QSize
from src.ui.styles import upload_button_styleResize, resize_button
from src.controllers.FIleOperatorResize import FileOperator


class ResizeConfirmationDialog(QDialog):
    def __init__(self, format, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmer redimensionnement")
        self.setFixedSize(300, 150)

        # Layout for the dialog
        layout = QVBoxLayout(self)

        # Label for the message
        self.message_label = QLabel(f"Voulez vous redimensionner les fichiers sélectionnés en {format} ?", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)  # Enable word wrap to avoid text being cut off
        layout.addWidget(self.message_label)

        # Buttons
        button_layout = QHBoxLayout()
        
        # Yes button
        self.yes_button = QPushButton("Oui", self)
        self.yes_button.clicked.connect(self.accept)
        button_layout.addWidget(self.yes_button)

        # No button
        self.no_button = QPushButton("Non", self)
        self.no_button.clicked.connect(self.reject)
        button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)

    def exec_(self):
        """Executes the dialog and returns the result"""
        return super().exec_()


class ResizePdf(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        self.setWindowTitle("Packet Weight Checker")
        self.on_hold = []
        self.names = {}
        self.currently_selected = {}
        self.currently_selected_label = f"Actuellement {len(self.currently_selected)} fichiers sélectionnés"

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        """Operator class that holds the methods for pdf"""
        self.operator = FileOperator(parent=central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins for full-width design
        main_layout.setSpacing(0)

        # Header Section
        header = QLabel("PDF RESIZE")
        header.setStyleSheet(f"""
            background-color: #242424;
            color: #E84545;
            font-size: 26px;
            font-weight: bold;
            padding: 15px;
            border-bottom: 2px solid #e55414;
        """)
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(60)
        main_layout.addWidget(header)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet(f"""
            background-color: #2f2f2f;
            border-right: 2px solid #e55414;
        """)
        sidebar.setFixedWidth(300)

        # Sidebar Layout
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)

        upload_bl_button = QPushButton("Télécharger PDF")
        upload_bl_button.setStyleSheet(upload_button_styleResize)
        """This will be where the user clicks to upload files from computer. 
            files need to be a certain format to be valid (depending on user specifications)
            for this app they will be order invoices with articles, this is where we will get our quantities and
            articles that have been shipped, and from there our estimated weight for a package"""
        upload_bl_button.clicked.connect(self.upload_files_and_render)

        sidebar_layout.addWidget(upload_bl_button)

        # Scrollable area to show file names
        self.file_names_scroll_area = QScrollArea()
        self.file_names_scroll_area.setWidgetResizable(True)
        self.file_names_widget = QWidget()
        self.file_names_layout = QVBoxLayout(self.file_names_widget)

        self.file_names_scroll_area.setWidget(self.file_names_widget)
        sidebar_layout.addWidget(self.file_names_scroll_area)
        content_layout.addWidget(sidebar)

        # Main Area
        main_area = QFrame()
        main_area.setStyleSheet("""
            background-color: #f9f9f9;
        """)

        # Main area layout
        main_area_layout = QVBoxLayout(main_area)
        main_area_layout.setContentsMargins(20, 20, 20, 20)
        main_area_layout.setSpacing(10)

        # Add description labels
        description_label = QLabel("Sélectionnez un format pour redimensionner votre PDF")
        description_label.setStyleSheet("""
            color: #333;
            font-size: 14px;
            font-weight: normal;
        """)
        description_label.setAlignment(Qt.AlignCenter)
        main_area_layout.addWidget(description_label, alignment=Qt.AlignTop)

        # Add small label above buttons
        self.files_selected_label = QLabel(self.currently_selected_label)   #Needs a class with a refresh method !!maybe!!
        self.files_selected_label.setStyleSheet("""
            color: #555;
            font-size: 12px;
        """)
        self.files_selected_label.setAlignment(Qt.AlignCenter)
        main_area_layout.addWidget(self.files_selected_label)

        # Button Grid Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Format buttons
        ResizeToA4Button = QPushButton("A4")
        ResizeToA3Button = QPushButton("A3")
        ResizeToA2Button = QPushButton("A2")
        ResizeToA1Button = QPushButton("A1")
        ResizeToA0Button = QPushButton("A0")

        ResizeToA4Button.setStyleSheet(resize_button)
        ResizeToA3Button.setStyleSheet(resize_button)
        ResizeToA2Button.setStyleSheet(resize_button)
        ResizeToA1Button.setStyleSheet(resize_button)
        ResizeToA0Button.setStyleSheet(resize_button)

        ResizeToA4Button.clicked.connect(lambda: self.ask_for_resize("A4"))
        ResizeToA3Button.clicked.connect(lambda: self.ask_for_resize("A3"))
        ResizeToA2Button.clicked.connect(lambda: self.ask_for_resize("A2"))
        ResizeToA1Button.clicked.connect(lambda: self.ask_for_resize("A1"))
        ResizeToA0Button.clicked.connect(lambda: self.ask_for_resize("A0"))

        button_layout.addWidget(ResizeToA4Button)
        button_layout.addWidget(ResizeToA3Button)
        button_layout.addWidget(ResizeToA2Button)
        button_layout.addWidget(ResizeToA1Button)
        button_layout.addWidget(ResizeToA0Button)

        main_area_layout.addLayout(button_layout)

        # Add Download button below the format buttons
        download_button = QPushButton("Télécharger")
        download_button.setStyleSheet(resize_button)
        download_button.clicked.connect(lambda: print(self.currently_selected))

        main_area_layout.addWidget(download_button, alignment=Qt.AlignCenter)

        content_layout.addWidget(main_area)
        main_layout.addLayout(content_layout)

        # Footer Section
        footer = QLabel("© 2024 SaiToolBox | All Rights Reserved")
        footer.setStyleSheet(f"""
            background-color: #2f2f2f;
            color: white;
            font-size: 14px;
            padding: 10px;
            border-top: 2px solid #e55414;
        """)
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        main_layout.addWidget(footer)

        # Render on memory
        self.operator.folder_reader(self.on_hold)
        self.render_on_hold(self.file_names_layout)

        # Center the window on the screen
        self.center_window()

    def upload_files_and_render(self):
        self.operator.upload_files(self)
        self.operator.folder_reader(self.on_hold)
        self.render_on_hold(self.file_names_layout)

    def render_on_hold(self, parent):
            # Clear existing widgets
            for i in reversed(range(parent.count())):
                widget = parent.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            # Add new widgets
            for file_name in reversed(self.on_hold):  # Iterate over items in self.on_hold
                name = ListItem(text=file_name)
                self.names[name.name] = name
                parent.addWidget(name)
                name.selection_changed.connect(self.handle_selection_changed) 
            self.files_selected_label.setText(f"Actuellement {len(self.currently_selected)} fichiers sélectionnés")
        

    def handle_selection_changed(self, file_name, selected):
        """This method updates the currently_selected dictionary and label."""
        if selected:
            self.currently_selected[file_name] = True
        else:
            if file_name in self.currently_selected:
                del self.currently_selected[file_name]
        self.files_selected_label.setText(f"Actuellement {len(self.currently_selected)} fichiers sélectionnés")

    def ask_for_resize(self, format):
        if len(self.currently_selected) == 0:
            QMessageBox.warning(self, "Aucun fichier sélectionné", "Veuillez sélectionner des fichiers à redimensionner.")
        else:
            # Create and show custom confirmation dialog
            dialog = ResizeConfirmationDialog(format, self)
            result = dialog.exec_()

            # Check dialog result
            if result == QDialog.Accepted:  # User clicked 'Yes'
                self.operator.resizeFiles(format, self.currently_selected)
                QMessageBox.information(self, "Redimensionnement réussi", f"Les fichiers ont été redimensionnés en {format}.")
            else:  # User clicked 'No'
                print("User selected 'No' or canceled.")


    def center_window(self):
        """Visual only, this centers the window on the screen when opened"""
        # Get screen geometry (the dimensions of the screen)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        # Get the dimensions of the main window
        window_width = self.width()
        window_height = self.height()
        # Calculate the position to center the window
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        # Move the window to the calculated position
        self.move(x, y)



                