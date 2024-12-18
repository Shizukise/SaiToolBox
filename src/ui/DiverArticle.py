import os,subprocess, platform
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QMainWindow,QFrame,QApplication,QMessageBox,QDialog
)
from PySide6.QtCore import Qt
from src.controllers.DiveScript import DiverScraper
from src.controllers.SendEmail import send_email
import pandas as pd
from src.ui.styles import *
from src.utils.EmailCredPopUp import LoginDialog

class Dive(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        self.setWindowTitle("DIVE")
        self.current_data = None
        self.output_folder = r"/home/galopin/Wa Its/src/data/DiveOutput"  # Change path
        file_name = "rapport_commandes_specifiques.xlsx"
        self.file_path = os.path.join(self.output_folder, file_name)
        self.setStyleSheet(window_style)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
            }
        """)

        header = QLabel("DIVE Tool")
        header.setStyleSheet("""
            QLabel {
                background-color: #2E2E2E;
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                border-bottom: 2px solid #00ADB5;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(60)
        main_layout.addWidget(header)

        input_section = QFrame()
        input_section.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: #CCCCCC;
                font-size: 14px;
                margin-bottom: 5px;
            }
            QLineEdit {
                background-color: #3E3E3E;
                color: white;
                font-size: 14px;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #00ADB5;
            }
            QComboBox {
                background-color: #3E3E3E;
                color: white;
                font-size: 14px;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #3E3E3E;
                color: white;
                selection-background-color: #00ADB5;
            }
        """)
        input_layout = QVBoxLayout(input_section)

        identifiant_label = QLabel("Identifiant:")
        self.identifiant_input = QLineEdit()
        self.identifiant_input.setPlaceholderText("Enter your identifiant")
        input_layout.addWidget(identifiant_label)
        input_layout.addWidget(self.identifiant_input)

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        input_layout.addWidget(password_label)
        input_layout.addWidget(self.password_input)

        team_label = QLabel("Select Team:")
        self.team_selector = QComboBox()
        self.team_selector.addItems(["Tous","Jeremy", "Tepea", "Aurelien"])
        input_layout.addWidget(team_label)
        input_layout.addWidget(self.team_selector)

        main_layout.addWidget(input_section)

        button_section = QFrame()
        button_layout = QVBoxLayout(button_section)

        top_row_layout = QHBoxLayout()
        run_button = QPushButton("Run Script")
        self.generate_button = QPushButton("Generate File")
        self.generate_button.setDisabled(True)
        self.send_email_button = QPushButton("Send via email")
        self.send_email_button.setDisabled(True)

        run_button.setStyleSheet("""
            QPushButton {
                background-color: #00ADB5;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px 24px;
                border: none;
            }
            QPushButton:hover {
                background-color: #009A9C;
            }
            QPushButton:pressed {
                background-color: #007B7C;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #666666;
                border: none;
            }
        """)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #00ADB5;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px 24px;
                border: none;
            }
            QPushButton:hover {
                background-color: #009A9C;
            }
            QPushButton:pressed {
                background-color: #007B7C;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #666666;
                border: none;
            }
        """)
        self.send_email_button.setStyleSheet("""
            QPushButton {
                background-color: #00ADB5;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px 24px;
                border: none;
            }
            QPushButton:hover {
                background-color: #009A9C;
            }
            QPushButton:pressed {
                background-color: #007B7C;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #666666;
                border: none;
            }
        """)

        run_button.clicked.connect(lambda: self.run_script(generate_button=self.generate_button))
        self.generate_button.clicked.connect(self.generate_file)
        self.send_email_button.clicked.connect(self.send_email_btn_method)

        top_row_layout.addWidget(run_button)
        top_row_layout.addWidget(self.generate_button)
        top_row_layout.addWidget(self.send_email_button)
        button_layout.addLayout(top_row_layout)

        download_button = QPushButton("Telecharger Rapport")
        download_button.setFixedSize(400, 45)
        download_button.setStyleSheet("""
            QPushButton {
                background-color: #4287f5;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px 24px;
                border: none;
            }
            QPushButton:hover {
                background-color: #306ecc;
            }
            QPushButton:pressed {
                background-color: #244b8a;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #666666;
                border: none;
            }
        """)
        download_button.clicked.connect(lambda: self.open_folder())

        centered_layout = QHBoxLayout()
        centered_layout.addStretch()
        centered_layout.addWidget(download_button)
        centered_layout.addStretch()

        button_layout.addLayout(centered_layout)
        main_layout.addWidget(button_section)

        footer = QLabel("© 2024 SaiToolBox | All Rights Reserved")
        footer.setStyleSheet("""
            QLabel {
                color: #CCCCCC;
                font-size: 12px;
                background-color: #1E1E1E;
                padding: 5px;
            }
        """)
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        main_layout.addWidget(footer)

        self.center_window()

    def run_script(self,generate_button):
        # Placeholder functionality
        identifiant = self.identifiant_input.text()
        password = self.password_input.text()
        team = self.team_selector.currentText()
        print(f"Running script with identifiant: {identifiant}, team: {team}")
        scraper = DiverScraper(username=identifiant,password=password,team=team)
        self.current_data = scraper.run_script()
        generate_button.setDisabled(False)

    def generate_file(self):
        if self.current_data:
            data_list = []
            for commande in self.current_data:
                for article in commande["Articles Spécifiques"]:
                    data_list.append({
                        "Référence": commande["Référence"],
                        "Article": article["Description"],
                        "Quantité": article["Quantité"]
                    })
            df = pd.DataFrame(data_list)
            with pd.ExcelWriter(self.file_path, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Commandes")
                workbook = writer.book
                worksheet = writer.sheets["Commandes"]
                for idx, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    column_letter = worksheet.cell(row=1, column=idx + 1).column_letter 
                    worksheet.column_dimensions[column_letter].width = max_len
            rapport_path = r"/home/galopin/Wa Its/rapport_commandes_specifiques.xlsx"  #Change path
            self.send_email_button.setDisabled(False)
            self.send_email_button.clicked.connect(lambda : self.send_email_btn_method)

    def send_email_btn_method(self):
        rapport_path = r"/home/galopin/Wa Its/rapport_commandes_specifiques.xlsx"
        if not self.generate_button.isEnabled()  or not os.path.exists(rapport_path):
            QMessageBox(self,"Aucun fichier n'a encore été généré", "veuillez exécuter le script.")
        else:
            try:
                creds = LoginDialog().exec_()
                if creds == QDialog.Accepted:
                    email, password = creds.get_credentials()
                    send_email(email,password,rapport_path)
            except Exception as e:
                print (f"Exception occurred : {e}")
                
    def open_folder(self):
        if platform.system() == 'Windows':
            os.startfile(self.output_folder)
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', self.output_folder])
        else:
            print("Unsupported OS")

    def center_window(self):
        """Centers the window on the screen when opened."""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_width = self.width()
        window_height = self.height()
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.move(x, y)
