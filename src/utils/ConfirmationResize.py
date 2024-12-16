from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout,QPushButton
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
        
