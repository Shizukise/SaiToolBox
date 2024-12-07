from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt

class StyledListItem(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 150);  /* Black with low opacity */
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)