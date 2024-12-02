from PySide2.QtWidgets import QPushButton, QWidget, QVBoxLayout, QMainWindow, QApplication
from PySide2.QtCore import QSize

#### Packet weight checker : This tool will take a pdf file as input (Order Invoice), and will calculate the weight of a package based on ordered items #####

class PacketWeightChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        button = QPushButton("Hello!")
        self.setCentralWidget(button)
        self.center_window()

    def center_window(self):
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