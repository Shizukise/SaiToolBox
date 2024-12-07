import sys
import os
from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
from src.ui.ButtonShortcut import ShortcutButton
from src.ui.PacketWeightCheck import PacketWeightChecker

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'/home/galopin/Área de Trabalho/Projects/Wa Its/Wa_its_venv/lib/python3.11/site-packages/PySide2/Qt/plugins/platforms'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ToolBox")
        self.setFixedSize(QSize(900, 500))

       
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)

       
        button_container = QVBoxLayout()
        button_container.setAlignment(Qt.AlignCenter)

      
        button_row_1 = QHBoxLayout()
        button_row_1.setSpacing(20)  # Space between buttons
        button_row_2 = QHBoxLayout()
        button_row_2.setSpacing(20)

       
        button1 = ShortcutButton(text="OBLI", window=self, widget=packet_weight_checker, color="#ff661a")
        button2 = ShortcutButton(text="RESIZE", window=self, widget=resize_pdf,  color="#E84545")
        button3 = ShortcutButton(text="PERCE", window=self, color="#e600e6")
        button4 = ShortcutButton(text="DIVE", window=self, color="#00ADB5")
        button5 = ShortcutButton(text="Widget5", window=self)
        button6 = ShortcutButton(text="Widget6", window=self)

       
        button_row_1.addWidget(button1)
        button_row_1.addWidget(button2)
        button_row_1.addWidget(button3)
        button_row_2.addWidget(button4)
        button_row_2.addWidget(button5)
        button_row_2.addWidget(button6)

     
        button_container.addLayout(button_row_1)
        button_container.addLayout(button_row_2)

       
        main_layout.addLayout(button_container)

       
        footer = self.create_footer()
        main_layout.addWidget(footer)

       
        self.setCentralWidget(main_widget)
        self.center_window()

    def create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(30)
        footer.setStyleSheet("""
            QFrame {
                background-color: #393E46; /* Footer background color */
                color: white;             /* Footer text color */
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
        """)
        footer_layout = QVBoxLayout(footer)
        footer_layout.setAlignment(Qt.AlignCenter)

        footer_label = QLabel("© 2024 SaiToolBox | All Rights Reserved")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(footer_label)

        return footer

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
resize_pdf = ResizePdf()

# Create the main window instance
window = MainWindow()
window.show()
app.exec_()
