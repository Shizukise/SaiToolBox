from PySide2.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QMainWindow,QFrame,QApplication,
)
from PySide2.QtCore import Qt
from src.controllers.DiveScript import DiverScraper
import pandas as pd
from src.ui.styles import *

class Dive(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        self.setWindowTitle("DIVE")
        self.current_data = None

         # Main layout for the window
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Set margins to zero to eliminate gaps on the sides
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QLabel("DIVE Tool")
        header.setStyleSheet(header_style)
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(60)
        main_layout.addWidget(header)

        # Inputs Section
        input_section = QFrame()
        input_section.setStyleSheet(input_style)
        input_layout = QVBoxLayout(input_section)

        # Identifiant
        identifiant_label = QLabel("Identifiant:")
        self.identifiant_input = QLineEdit()
        self.identifiant_input.setPlaceholderText("Enter your identifiant")
        input_layout.addWidget(identifiant_label)
        input_layout.addWidget(self.identifiant_input)

        # Password
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        input_layout.addWidget(password_label)
        input_layout.addWidget(self.password_input)

        # Team Selection
        team_label = QLabel("Select Team:")
        self.team_selector = QComboBox()
        self.team_selector.setStyleSheet(combo_box_style)
        self.team_selector.addItems(["Tous", "Jeremy", "Tepea", "Aurelien"])
        input_layout.addWidget(team_label)
        input_layout.addWidget(self.team_selector)

        main_layout.addWidget(input_section)

        # Button Section
        button_section = QFrame()
        button_layout = QHBoxLayout(button_section)

        run_button = QPushButton("Run Script")
        generate_button = QPushButton("Generate File")
        generate_button.setDisabled(True)
        run_button.setStyleSheet(run_button_style)
        generate_button.setStyleSheet(run_button_style)
        run_button.clicked.connect(lambda : self.run_script(generate_button=generate_button))
        generate_button.clicked.connect(self.generate_file)

        button_layout.addWidget(run_button)
        button_layout.addWidget(generate_button)

        main_layout.addWidget(button_section)

        # Footer
        footer = QLabel("© 2024 SaiToolBox | All Rights Reserved")
        footer.setStyleSheet(footer_style)
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
            with pd.ExcelWriter("rapport_commandes_specifiques_via_DOM.xlsx", engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Commandes")
                workbook = writer.book
                worksheet = writer.sheets["Commandes"]
                for idx, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    column_letter = worksheet.cell(row=1, column=idx + 1).column_letter 
                    worksheet.column_dimensions[column_letter].width = max_len

    def center_window(self):
        """Centers the window on the screen when opened."""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_width = self.width()
        window_height = self.height()
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.move(x, y)
