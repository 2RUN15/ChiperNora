from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction, QPixmap
from ServiceWindow.service_win_app import ServiceWindow
import sys

class MainService(ServiceWindow):
    def __init__(self):
        super().__init__()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    service = MainService()
    sys.exit(app.exec())