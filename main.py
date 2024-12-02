import sys
import os
from PySide2.QtCore import QSize, Qt, QCoreApplication
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout

from src.ui.ButtonShortcut import ShortcutButton
from src.ui.PacketWeightCheck import PacketWeightChecker

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'/home/galopin/Área de Trabalho/Projects/Wa Its/Wa_its_venv/lib/python3.11/site-packages/PySide2/Qt/plugins/platforms'

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ToolBox")
        self.setFixedSize(QSize(900, 500))

        main_widget = QWidget(self)
        layout = QGridLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)  # Add padding around the layout
        layout.setSpacing(20)  # Space between widgets
        layout.setAlignment(Qt.AlignCenter)  # Center the layout contents
        self.setCentralWidget(main_widget)

        button1 = ShortcutButton(text="Packet Weight Check", window=self, widget=packet_weight_checker, color="#00ADB5")
        button2 = ShortcutButton(text="Pdf Resize", window=self, color="#E84545")
        button3 = ShortcutButton(text="Add piercing contour", window=self)
        button4 = ShortcutButton(text="Widget4", window=self)
        button5 = ShortcutButton(text="Widget5", window=self)
        button6 = ShortcutButton(text="Widget6", window=self)

        layout.addWidget(button1, 0, 0)
        layout.addWidget(button2, 0, 1)
        layout.addWidget(button3, 0, 2)
        layout.addWidget(button4, 1, 0)
        layout.addWidget(button5, 1, 1)
        layout.addWidget(button6, 1, 2)

        self.center_window() # Explicitly call the center_window method to center the window when the class instance is created

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

# Main app, this runs the main loop! no widgets can be defined before this runs (this means no standalone widgets can be defined in other files)
app = QApplication([])

# This creates the widget for the packet weight checker
packet_weight_checker = PacketWeightChecker()

# Create the main window instance
window = MainWindow()

# Show the window
window.show()
app.exec_()
