from PyQt6.QtWidgets import QMessageBox
from datapack import warningmsg

class ReturnErr(QMessageBox):
    def __init__(self,error):
        self.error = error
        super().__init__()
        self.setWindowTitle("ERROR!")
        self.setText(f"{self.error}")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Critical)

class WarningMess(QMessageBox):
    def __init__(self, conf: warningmsg):
        super().__init__()
        self.setWindowTitle(f"{conf.window_tittle}")
        self.setText(f"{conf.text}")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)