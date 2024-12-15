from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtCore import QSize

class ShortcutButton(QPushButton):

    def __init__(self,text,window,widget=None,color="#393E46",parent=None):  #The construct accepts the main window , and the widget that will be opened when clicked
        super().__init__(text,parent)

        self.main_window = window
        self.widget = widget
        self.color = color

        self.setFixedHeight(40)
        self.setFixedWidth(100)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: #007C91;  /* Slightly darker shade on hover */
            }}
            QPushButton:pressed {{
                background-color: #005F6B;  /* Even darker when pressed */
            }}
        """)

        self.clicked.connect(self.the_button_was_clicked)

    def the_button_was_clicked(self):
        if self.widget != None:
            self.widget.show()
                



