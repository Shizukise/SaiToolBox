from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Qt,QSize, Signal

class ListItem(QLabel):
    clicked = Signal() 
    selection_changed = Signal(str, bool)  

    def __init__(self, text, selected=False):
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
        self.name = text

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  
            self.setSelected()
        super().mousePressEvent(event)

    def setSelected(self):
        # Change selection style and emit signal with updated selection
        if self.selected:
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
        else:
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
        
        # Emit the signal with the file name and selection state
        self.selection_changed.emit(self.name, self.selected)


            