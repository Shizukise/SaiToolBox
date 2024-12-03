from PySide2.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QFrame
)
from PySide2.QtCore import Qt, QSize


class PacketWeightChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 620)
        self.setWindowTitle("Packet Weight Checker")

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Header Section
        header = QLabel("OBLI")
        header.setStyleSheet(f"""
            background-color: #00ADB5;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(50)
        main_layout.addWidget(header)

        # Main Content Section
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        # Sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet(f"background-color: white;")
        sidebar.setFixedWidth(300)
        content_layout.addWidget(sidebar)

        check_weight_button = QPushButton("Verifié Poid",sidebar)
        check_weight_button.setGeometry(50,150,200,50)
        check_weight_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #00ADB5;
                        color: white;  
                        font-family: 'Arial', sans-serif;
                        font-weight: bold;
                        font-size: 16px;
                    }}

                    QPushButton:hover {{
                        background-color: #00f2ff;  
                        color: white; 
                    }}
                """)

        upload_bl_button = QPushButton("Upload Bl", sidebar)
        upload_bl_button.setGeometry(50,220,200,50)
        upload_bl_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #00ADB5;
                        color: white;  
                        font-family: 'Arial', sans-serif;
                        font-weight: bold;
                        font-size: 16px;
                    }}

                    QPushButton:hover {{
                        background-color: #00f2ff;  
                        color: white; 
                    }}
                """)

        # Main Area
        main_area = QFrame()
        main_area.setStyleSheet("background-color: white;")
        content_layout.addWidget(main_area)

        main_layout.addLayout(content_layout)

        # Footer Section
        footer = QLabel("© 2024 SaiToolBox | All Rights Reserved")
        footer.setStyleSheet(f"""
            background-color: #393E46;
            color: white;
            font-size: 14px;
            padding: 5px;
        """)
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(30)
        main_layout.addWidget(footer)

        # Center the window on the screen
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
