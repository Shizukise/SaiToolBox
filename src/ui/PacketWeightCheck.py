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
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins for full-width design
        main_layout.setSpacing(0)

        # Header Section
        header = QLabel("OBLI")
        header.setStyleSheet(f"""
            background-color: #ff661a;
            color: white;
            font-size: 26px;
            font-weight: bold;
            padding: 15px;
            border-bottom: 2px solid #e55414;
        """)
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(60)
        main_layout.addWidget(header)

        # Main Content Section
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet(f"""
            background-color: #2f2f2f;
            border-right: 2px solid #e55414;
        """)
        sidebar.setFixedWidth(300)

        # Sidebar Layout
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        # Sidebar Buttons
        check_weight_button = QPushButton("Check Weight")
        check_weight_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #ff661a;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #e55414;
            }}
            QPushButton:pressed {{
                background-color: #c44712;
            }}
        """)

        upload_bl_button = QPushButton("Upload BL")
        upload_bl_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #ff661a;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #e55414;
            }}
            QPushButton:pressed {{
                background-color: #c44712;
            }}
        """)

        # Add buttons to sidebar
        sidebar_layout.addWidget(check_weight_button)
        sidebar_layout.addWidget(upload_bl_button)
        sidebar_layout.addStretch()  # Push buttons to the top
        content_layout.addWidget(sidebar)

        # Main Area
        main_area = QFrame()
        main_area.setStyleSheet("""
            background-color: #f9f9f9;
        """)
        content_layout.addWidget(main_area)

        main_layout.addLayout(content_layout)

        # Footer Section
        footer = QLabel("© 2024 SaiToolBox | All Rights Reserved")
        footer.setStyleSheet(f"""
            background-color: #2f2f2f;
            color: white;
            font-size: 14px;
            padding: 10px;
            border-top: 2px solid #e55414;
        """)
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
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