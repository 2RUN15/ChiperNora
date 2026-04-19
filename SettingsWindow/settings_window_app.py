from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from SettingsWindow.settings_window_ui import Ui_SettingsDialog
from actions.func_main import file_read, path_join

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        
        #Style
        self.style_path = path_join(["SettingsWindow","style.qss"])
        self.styleqss = file_read(self.style_path)
        self.setStyleSheet(self.styleqss)