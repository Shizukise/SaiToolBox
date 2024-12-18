from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        self.email_label = QLabel("Email:", self)
        layout.addWidget(self.email_label)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Password:", self)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password) 
        layout.addWidget(self.password_input)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_credentials(self):
        """Return the email and password entered by the user."""
        return self.email_input.text(), self.password_input.text()