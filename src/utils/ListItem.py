from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Qt,QSize, Signal

class ListItem(QLabel):
    clicked = Signal()

    def __init__(self, text, selected = False):
        super().__init__(text)
        self.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border-radius: 5px;
                padding: 4px;
                font-size: 10px;
            }
        """)
        self.setFixedSize(QSize(250, 30))
        self.selected = selected

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  
            self.clicked.emit()  
        super().mousePressEvent(event)  

    def setSelected(self):
        if self.selected == False:
            self.setStyleSheet("""
            QLabel {
                background-color: #F96E2A; 
                color: white;
                border-radius: 5px;
                padding: 4px;
                font-size: 10px;
            }
        """)
            self.selected = True
        else:
            self.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border-radius: 5px;
                padding: 4px;
                font-size: 10px;
            }
        """)
            self.selected = False