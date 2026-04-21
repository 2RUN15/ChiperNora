from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from SettingsWindow.settings_window_ui import Ui_SettingsDialog
from actions.func_main import file_read, path_join, json_read, json_save, create_conf_json
from SettingsWindow.funcs import change_engine, re_change_engine
from actions.msgbox import ReturnErr, WarningMess
from actions.dialogs import chose_file
from SettingsWindow.settings_msgbox import *

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        
        #EmptyValues
        self.save_location = ""
        
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
        self.ui.cmb_engine.currentIndexChanged.connect(self.cmb_engine_api_change)
        self.ui.choose_file_btn.clicked.connect(self.get_file_location)
        
        #ViewConf
        self.cmb_engine_api_change(0)
        
    def save_config(self):
        try:
            cmb_engine = self.ui.cmb_engine.currentIndex()
            cmb_engine = change_engine(cmb_engine)
        
            api_key = self.ui.txt_api_key.text()
            if not api_key:
                return warn_api_key()
            
            if not self.save_location:
                return warn_save_loc
            
            word_limit = self.ui.spin_word_limit.text()

            self.api_conf["active_engine"] = cmb_engine
            if cmb_engine == "mymemory":
                self.api_conf["engines"][f"{cmb_engine}"]["email"] = api_key
            else:
                self.api_conf["engines"][f"{cmb_engine}"]["api_key"] = api_key
            self.api_conf["settings"]["word_limit"] = word_limit
            
            json_save(self.api_config_path, self.api_conf)
            self.close()
        
        except Exception as e:
            self.err = ReturnErr(e)
            self.err.exec()
    
    def reset_settings(self):
        create_conf_json(True)
    
    def cmb_engine_api_change(self, index):
        cmb_engine = change_engine(index)
        
        if cmb_engine == "mymemory":
            api_key = self.api_conf["engines"][f"{cmb_engine}"]["email"]    
        else:
            api_key = self.api_conf["engines"][f"{cmb_engine}"]["api_key"]
            
        word_limit = self.api_conf["settings"]["word_limit"]
        self.ui.txt_api_key.setText(api_key)
        self.ui.spin_word_limit.setValue(int(word_limit))
    
    def get_file_location(self):
        self.save_location = chose_file()
    