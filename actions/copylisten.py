from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication

class CopyListen(QObject):
    link_found = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.board = QApplication.clipboard()
        self.last_link = ""
        self.is_activate = False
        self.board.dataChanged.connect(self.send_signal)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_signal)
    
    def start(self):
        if self.is_activate == False:
            self.is_activate = True
            self.timer.start(1000)
    
    def stop(self):
        if self.is_activate:
            self.is_activate = False
            self.timer.stop()
        
    def send_signal(self):
        if not self.is_activate:
            return
        text = self.board.text()
        
        if text and self.last_link != text:
            self.last_link = text
            self.link_found.emit(text)