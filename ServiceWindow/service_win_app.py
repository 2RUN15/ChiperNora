from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction, QPixmap
from actions.func_main import path_join, get_active_engine
from SettingsWindow.settings_window_app import SettingsWindow
from API.translate_api.deepl_api import DeeplAPI

class ServiceWindow:
    def __init__(self):
        super().__init__()
        
        #NoneValus
        self.settingswin = None
        self.savedata = None
        self.downmode = None
        
        self.icon = path_join(["icons","mainico.png"])
        
        #TrayMenu
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(self.icon))
        self.menu = QMenu()
        
        #Action Ekleme
        self.action_actv = QAction("Activate")
        self.action_exit = QAction("Exit")
        self.action_settings = QAction("Settings")
    
    
        #Actions Bağlantıları
        
            #Activate
        self.action_actv.setCheckable(True)
        self.action_actv.setChecked(True)
        self.action_actv.triggered.connect(self.app_stat)
        
            #Settings
        self.action_settings.triggered.connect(self.open_settings)
        
            #Exit
        self.action_exit.triggered.connect(QApplication.instance().quit)
        
        #Action'u menüye ekleme
        self.menu.addAction(self.action_actv)
        self.menu.addAction(self.action_settings)
        self.menu.addSeparator()
        self.menu.addAction(self.action_exit)
        
        #Çalıştırma
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        
        #Threads
        self.active_engine = get_active_engine()
        if self.active_engine == "deepl":
            self.worker = DeeplAPI()
            self.worker.start()
        
    def _on_settings_closed(self):
        self.settingswin = None
        
    def app_stat(self, boolval):
        if boolval and self.active_engine == "deepl":
            self.worker.start()
        elif not boolval and self.active_engine == "deepl":
            self.worker.stop()
    
    def open_settings(self):
        if hasattr(self, "settingswin") and self.settingswin is not None:
            self.settingswin.activateWindow()
            self.settingswin.raise_()
            return
            
        self.settingswin = SettingsWindow()
        
        self.settingswin.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.settingswin.destroyed.connect(self._cloesd_settings) 
        
        self.settingswin.show()
    
    def _cloesd_settings(self):
        self.settingswin = None
    