from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor

class TranslationPopup(QLabel):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.ToolTip
        )
        
        self.setStyleSheet("""
            QLabel {
                background-color: #1E1E24;
                color: #00D2FF;
                border: 1px solid #33333C;
                border-radius: 6px;
                padding: 8px 12px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        self.hide()

    def show_at_cursor(self, text):
        self.setText(text)
        self.adjustSize() 
        
        # Farenin global koordinatlarını al
        cursor_pos = QCursor.pos()
        
        self.move(cursor_pos.x() + 15, cursor_pos.y() + 15)
        
        self.show()
        
        QTimer.singleShot(2500, self.hide)
        