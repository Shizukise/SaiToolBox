import os, shutil
from PySide2.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFileDialog,QMessageBox
)
from PySide2.QtCore import Qt, QSize
from src.ui.styles import package_weight_check_button_style, upload_button_style

class PacketWeightChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        self.setWindowTitle("Packet Weight Checker")

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

        # Sidebar Buttons
        ##Check weight button
        check_weight_button = QPushButton("Verifiée Poids")
        check_weight_button.setStyleSheet(package_weight_check_button_style)
        """This button runs on all loaded pdf files, and extracts the weight calculated from each one
            being then rendered on the main area at the right side of the screen. Or, it will run on selected files only."""
        check_weight_button.clicked.connect(self.operator.calculate_weights_from_pdf)
        

        ##Upload files button
        upload_bl_button = QPushButton("Upload BL")
        upload_bl_button.setStyleSheet(upload_button_style)
        """This will be where the user clicks to upload files from computer. 
            files need to be a certain format to be valid (depending on user specifications)
            for this app they will be order invoices with articles, this is where we will get our quantities and
            articles that have been shipped, and from there our estimated weight for a package"""
        upload_bl_button.clicked.connect(lambda: self.operator.upload_files(self))

        # Add buttons to sidebar
        sidebar_layout.addWidget(check_weight_button)
        sidebar_layout.addWidget(upload_bl_button)
        sidebar_layout.addStretch()  # Push buttons to the top
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

        # Center the window on the screen
        self.center_window()

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

    def __init__(self,parent,test="TEST"):
        self.test = test
        self.upload_folder = "src/data/BlInMemory"
        self.parent = parent
    
    def calculate_weights_from_pdf(self):
        print(self.test)

    def upload_files(self, parent):
        # Open a file dialog to select files
        file_path, _ = QFileDialog.getOpenFileName(parent, "Sélectionnez un fichier", "", ";Fichiers PDF (*.pdf)")

        if file_path:
            try:
                # Get the file name and construct the destination path
                file_name = os.path.basename(file_path)
                destination_path = os.path.join(self.upload_folder, file_name)

                # Ensure the upload folder exists
                os.makedirs(self.upload_folder, exist_ok=True)

                # Copy the file to the destination folder
                shutil.copy(file_path, destination_path)

                # Show success message
                QMessageBox.information(parent, "Téléversement réussi", f"Le fichier a été téléversé.")
            except Exception as e:
                # Show error message if something goes wrong
                QMessageBox.critical(parent, "Échec du téléversement", f"Une erreur s'est produite : {str(e)}")
        else:
            QMessageBox.warning(parent, "Aucun fichier sélectionné", "Veuillez sélectionner un fichier à téléverser.")

