from PyQt6.QtWidgets import QMessageBox
from datapack import warningmsg

#Hata mesajı fırlatır
class ReturnErr(QMessageBox):
    def __init__(self,error):
        self.error = error
        super().__init__()
        self.setWindowTitle("ERROR!")
        self.setText(f"{self.error}")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Critical)

#Uyarı mesajı fırlatır
class WarningMess(QMessageBox):
    def __init__(self, conf: warningmsg):
        super().__init__()
        self.setWindowTitle(f"{conf.window_tittle}")
        self.setText(f"{conf.text}")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)

class ReturnErr_Ok_No(QMessageBox):
    def __init__(self,error):
        self.error = error
        super().__init__()
        self.setWindowTitle("ERROR!")
        self.setText(f"{self.error}")
        self.setStandardButtons(self.StandardButton.Yes | self.StandardButton.No)
        self.setIcon(self.Icon.Critical)