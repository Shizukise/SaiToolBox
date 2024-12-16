from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QLabel

class ListItem(QLabel):
    clicked = Signal()
    selection_changed = Signal(str, bool)

    def __init__(self, text, selected=False):
        super().__init__(text)
        self.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: #ECF0F1;
                border: none;
                padding: 4px 8px;
                font-size: 14px;
            }
        """)
        self.setFixedSize(QSize(250, 35))  # Reduced height for compact list
        self.selected = selected
        self.name = text
        self.setAttribute(Qt.WA_Hover)

    def enterEvent(self, event):
        """Hover effect for the item."""
        self.setStyleSheet("""
            QLabel {
                background-color: #34495E;
                color: #ECF0F1;
                border: none;
                padding: 4px 8px;
                font-size: 14px;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Revert to the default style when hover ends."""
        self.update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle click events."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            self.toggle_selection()
        super().mousePressEvent(event)

    def toggle_selection(self):
        """Toggle the selection state and update style."""
        self.selected = not self.selected
        self.update_style()
        self.selection_changed.emit(self.name, self.selected)

    def update_style(self):
        """Apply the appropriate style based on selection state."""
        if self.selected:
            self.setStyleSheet("""
                QLabel {
                    background-color: #FF6F61;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    font-size: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    background-color: #2C3E50;
                    color: #ECF0F1;
                    border: none;
                    padding: 4px 8px;
                    font-size: 14px;
                }
            """)
