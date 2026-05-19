from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction, QPixmap
from actions.func_main import get_first_open, get_resource_path, get_worker_mode
from actions.system_permissions import check_permissions
from SettingsWindow.settings_window_app import SettingsWindow
from API.translate_api.translate_app_api import TranslateAPI
from VisualBased.visual_based_app import VisualBased
import platform

#Python ikonunu kaldırır
def set_mac_dock_icon_visible(visible):
    if platform.system() == "Darwin":
        try:
            from AppKit import NSApp, NSApplicationActivationPolicyRegular, NSApplicationActivationPolicyAccessory
            
            if visible:
                NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
            
            else:
                NSApp.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        except ImportError:
            pass

class ServiceWindow(QObject):
    def __init__(self):
        super().__init__()
        
        #DockVisible
        set_mac_dock_icon_visible(False)
        
        #CheckPermissions
        check_permissions()

        QApplication.instance().setQuitOnLastWindowClosed(False)
        
        #NoneValus
        self.settingswin = None
        self.savedata = None
        self.downmode = None
        
        self.icon = get_resource_path("icons","mainico.png")
        
        #TrayMenu
        self.tray = QSystemTrayIcon(self)
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
        
        #First Open
        self.first_open = get_first_open()
                
        #Threads
        if not self.first_open:
            self.open_settings()
        else:
            self.worker_mode = get_worker_mode()
            self.start_worker()
        
    def _on_settings_closed(self):
        self.settingswin = None
        
    def app_stat(self, boolval):
        if boolval:
            self.worker.start()
        elif not boolval:
            self.worker.stop()
    
    def open_settings(self):
        set_mac_dock_icon_visible(True)
        if hasattr(self, "worker") and self.worker:         
            self.worker.stop()
        if hasattr(self, "settingswin") and self.settingswin is not None:
            self.settingswin.activateWindow()
            self.settingswin.raise_()
            return
            
        self.settingswin = SettingsWindow()
        
        self.settingswin.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.settingswin.destroyed.connect(self._cloesd_settings)
        self.settingswin.settings_changed.connect(self.change_settings)
        
        self.settingswin.show()
    
    def _cloesd_settings(self):
        set_mac_dock_icon_visible(False)
        self.settingswin = None
        if hasattr(self, "worker") and self.worker:         
            self.worker.start()
    
    def change_settings(self, boolValue):
        if boolValue:
            self.worker_mode = get_worker_mode()
            self.start_worker()

    def start_worker(self):
        if hasattr(self, "worker") and self.worker:
            self.worker.stop()

        if self.worker_mode == "tb":
            self.worker = TranslateAPI()

        self.worker.update_settings()
        self.worker.start()
