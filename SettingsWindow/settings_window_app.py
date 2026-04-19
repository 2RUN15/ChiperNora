from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from SettingsWindow.settings_window_ui import Ui_SettingsDialog
from actions.func_main import file_read, path_join, json_read, json_save, create_conf_json
from actions.msgbox import ReturnErr, WarningMess
from datapack import warningmsg

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        
        #Style
        self.style_path = path_join(["SettingsWindow","style.qss"])
        self.styleqss = file_read(self.style_path)
        self.setStyleSheet(self.styleqss)
        
        #API_Config
        self.api_config_path = path_join(["API","config.json"])
        self.api_conf = json_read(self.api_config_path)
        
        #Butto_Actions
        self.ui.btn_save.clicked.connect(self.save_config)
        self.ui.reset_set_btn.clicked.connect(self.reset_settings)
    
    def save_config(self):
        try:
                
            cmb_engine = self.ui.cmb_engine.currentIndex()
            if cmb_engine == 0:
                cmb_engine = "mymemory"
            elif cmb_engine == 1:
                cmb_engine = "deepl"
            elif cmb_engine == 2:
                cmb_engine == "google"
        
            api_key = self.ui.txt_api_key.text()
            if not api_key:
                return self.warn_api_key()
            
            word_limit = self.ui.spin_word_limit.text()

            self.api_conf["active_engine"] = cmb_engine
            self.api_conf["engines"][f"{cmb_engine}"]["api_key"] = api_key
            self.api_conf["settings"]["word_limit"] = word_limit
            
            json_save(self.api_config_path, self.api_conf)
            self.close()
        
        except Exception as e:
            self.err = ReturnErr(e)
            self.err.exec()
    
    def reset_settings(self):
        create_conf_json(True)
    
    def warn_api_key(self):
        warninmess_data = warningmsg(
            window_tittle="EMPTY API",
            text="Please make sure you enter your API key."
        )
        warningmsg_win = WarningMess(warninmess_data)
        warningmsg_win.exec()