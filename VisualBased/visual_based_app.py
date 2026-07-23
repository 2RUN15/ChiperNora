from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
from VisualBased.get_snipping import SnippingWidget
from actions.func_main import get_coordinates

class VisualBased(QObject):
    snipiing_screen_open_signal = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()

        self.hotkeys = {"<ctrl>+<shift>+t": self.trigger_process}

        self.listener = keyboard.GlobalHotKeys(self.hotkeys)
        
        self.coordinates = get_coordinates()

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()
        
        if self.listener.is_alive():
            self.listener.join()

    def update_settings(self):
        self.coordinates = get_coordinates()

    def trigger_process(self):
        self.snipiing_screen_open_signal.emit(True)