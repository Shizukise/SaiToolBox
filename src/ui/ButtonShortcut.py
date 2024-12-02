from PySide2.QtWidgets import QPushButton, QWidget, QVBoxLayout, QMainWindow
from PySide2.QtCore import QSize

class ShortcutButton(QWidget):

    def __init__(self,text,window,widget=None,color="#393E46"):  #The construct accepts the main window , and the widget that will be opened when clicked
        super().__init__()

        self.main_window = window
        self.widget = widget
        self.color = color

        button = QPushButton(f"{text}")
        button.setFixedSize(175,175)
        layout = QVBoxLayout(self)
        layout.addWidget(button)
        self.setLayout(layout)
        

        button.clicked.connect(self.the_button_was_clicked)
        button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #EEEEEE;
                        border: 2px solid {self.color};  /* Orange border */
                        color: {self.color};  /* Text color matches the border */
                        font-family: 'Arial', sans-serif;
                        font-weight: bold;
                        font-size: 16px;
                        border-radius: 8px;
                    }}

                    QPushButton:hover {{
                        background-color: {self.color};  /* Hover background becomes orange */
                        color: white;  /* Text becomes white */
                    }}
                """)
            
    def the_button_was_clicked(self):
        if self.widget != None:
            self.widget.show()
                



