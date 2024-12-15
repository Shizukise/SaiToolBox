import os, shutil
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFileDialog, QMessageBox, QScrollArea, QVBoxLayout
)
from src.utils.ListItem import ListItem
from PySide6.QtCore import Qt, QSize
from src.ui.styles import package_weight_check_button_style, upload_button_style

class PacketWeightChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        self.setWindowTitle("Packet Weight Checker")
        self.on_hold = []

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
        header = QLabel("OBLI")
        header.setStyleSheet(f"""
            background-color: #242424;
            color: #ff661a;
            font-size: 26px;
            font-weight: bold;
            padding: 15px;
            border-bottom: 2px solid #e55414;
        """)
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(60)
        main_layout.addWidget(header)

        # Main Content Section
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
        sidebar_layout.setSpacing(15)


        #development button
        development_buton = QPushButton("Develop")
        development_buton.clicked.connect(lambda: print(self.on_hold))

        # Sidebar Buttons
        ##Check weight button
        check_weight_button = QPushButton("Verifiée Poids")
        check_weight_button.setStyleSheet(package_weight_check_button_style)
        """This button runs on all loaded pdf files, and extracts the weight calculated from each one
            being then rendered on the main area at the right side of the screen. Or, it will run on selected files only."""
        check_weight_button.clicked.connect(lambda: self.operator.calculate_weights_from_pdf(parent_list=self.on_hold))
        

        ##Upload files button
        upload_bl_button = QPushButton("Upload BL")
        upload_bl_button.setStyleSheet(upload_button_style)
        """This will be where the user clicks to upload files from computer. 
            files need to be a certain format to be valid (depending on user specifications)
            for this app they will be order invoices with articles, this is where we will get our quantities and
            articles that have been shipped, and from there our estimated weight for a package"""
        upload_bl_button.clicked.connect(self.upload_files_and_render)

        # Add buttons to sidebar
        sidebar_layout.addWidget(check_weight_button)
        sidebar_layout.addWidget(upload_bl_button)
        sidebar_layout.addWidget(development_buton)   ####DEVELOPMENT################

        # Scrollable area to show file names
        self.file_names_scroll_area = QScrollArea()
        self.file_names_scroll_area.setWidgetResizable(True)
        self.file_names_widget = QWidget()
        self.file_names_layout = QVBoxLayout(self.file_names_widget)
        self.file_names_layout.setSpacing(10)

        self.file_names_scroll_area.setWidget(self.file_names_widget)
        sidebar_layout.addWidget(self.file_names_scroll_area)
        content_layout.addWidget(sidebar)

        # Main Area
        main_area = QFrame()
        main_area.setStyleSheet("""
            background-color: #f9f9f9;
        """)
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

         #render on memory
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
            parent.addWidget(name)  # Add to layout 

    def center_window(self):
        """ Visual only, this centers the window on the screen when opened"""
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


class FileOperator():

    def __init__(self, parent, test="TEST"):
        self.test = test
        self.upload_folder = "/home/galopin/Wa Its/src/data/BlInMemory"
        self.parent = parent
        self.pdf_files = []
    
    def calculate_weights_from_pdf(self,parent_list):
        self.pdf_files = []
        self.folder_reader(parent_list=parent_list)  #Carefull, now its making duplicates
        print(self.pdf_files)

    def upload_files(self, parent):
        """ Function connected to the upload file button.
            this opens a QFileDialog box that accepts pdfs only
            and later saves it to src/data/BlInMemory
        """
        
        file_paths, _ = QFileDialog.getOpenFileNames(parent, "Sélectionnez un fichier", "", ";Fichiers PDF (*.pdf)")
        if file_paths:
            try:
                for file_path in file_paths:
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(self.upload_folder, file_name)
                    # Ensure the upload folder exists
                    os.makedirs(self.upload_folder, exist_ok=True)
                    shutil.copy(file_path, destination_path)
                QMessageBox.information(parent, "Téléversement réussi", f"Le fichier a été téléversé.")
            except Exception as e:
                QMessageBox.critical(parent, "Exception", f"{str(e)}")
        else:
            QMessageBox.warning(parent, "Aucun fichier sélectionné", "Veuillez sélectionner un fichier à téléverseur.")

    def folder_reader(self,parent_list):
        for filename in os.listdir(self.upload_folder):
            if filename.endswith('.pdf'):                        #) and filename.startswith("BL")
                self.pdf_files.append(os.path.join(filename))    #self.upload_folder
                if filename not in parent_list:
                    parent_list.append(filename)