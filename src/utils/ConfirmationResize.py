from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout,QPushButton, QLineEdit,QMessageBox
from PySide6.QtCore import Qt
class ResizeConfirmationDialog(QDialog):

    """Dialog box for resize widget user confirmation.
        Expects user to click a format button with files selected,
        And asks the user if he is sure to resize."""
    
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
        """Executes the dialog and returns the result
           This either returns Accepted or Rejected.
           And later can be acessed by result.Accepted (bool)"""
        return super().exec_()
        


class ResizeOrientationDialog(QDialog):
    """Dialog box for resize widget user confirmation.
       Expects the user to input either Horizontal or Vertical
       and a custom format string. Returns both values.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choisir Orientation")
        self.setFixedSize(300, 200)
        
        # Layout for the dialog
        layout = QVBoxLayout(self)

        # Label for the message
        self.message_label = QLabel("Veuillez choisir l'orientation du fichier", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)  
        layout.addWidget(self.message_label)

        # Input field for custom format
        self.format_input = QLineEdit(self)
        self.format_input.setPlaceholderText("Custom Format")
        layout.addWidget(self.format_input)

        # Buttons for orientation
        button_layout = QHBoxLayout()

        # Horizontal button
        self.horizontal_button = QPushButton("Horizontal", self)
        self.horizontal_button.clicked.connect(self.set_horizontal)
        button_layout.addWidget(self.horizontal_button)

        # Vertical button
        self.vertical_button = QPushButton("Vertical", self)
        self.vertical_button.clicked.connect(self.set_vertical)
        button_layout.addWidget(self.vertical_button)

        layout.addLayout(button_layout)

        # Initialize variables to hold results
        self.orientation = None  # True for Horizontal, False for Vertical
        self.custom_format = ""

    def set_horizontal(self):
        """Set orientation to horizontal and accept dialog."""
        self.orientation = True
        self.custom_format = self.format_input.text().strip()
        if not self.custom_format:
            QMessageBox.warning(self, "Aucune taille sélectionnée", "Veuillez insérer une taille")
        else:
            self.accept()

    def set_vertical(self):
        """Set orientation to vertical and accept dialog."""
        self.orientation = False
        self.custom_format = self.format_input.text().strip()
        if not self.custom_format:
            QMessageBox.warning(self, "Aucune taille sélectionnée", "Veuillez insérer une taille")
        else:
            self.accept()

    def exec_(self):
        """Executes the dialog and returns result."""
        result = super().exec_()
        if result == QDialog.Accepted:
            return self.orientation, self.custom_format  # Return both orientation and format
        return None, None
