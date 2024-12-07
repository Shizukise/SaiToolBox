from PySide2.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFileDialog, QMessageBox, QScrollArea, QVBoxLayout
)
from PySide2.QtCore import Qt, QSize


class ResizePdf(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        self.setWindowTitle("Packet Weight Checker")
        self.on_hold = []

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins for full-width design
        main_layout.setSpacing(0)

        # Header Section
        header = QLabel("PDF RESIZE")
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
