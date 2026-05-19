from pynput import keyboard
from PyQt6.QtCore import QObject

class VisualBased(QObject):
    def __init__(self):
        super().__init__()
        
        self.hotkeys = {
            '<cmd>+<shift>+t': self.trigger_translation
        }
        
        self.listener = keyboard.GlobalHotKeys(self.hotkeys)
        
    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()
    
    def trigger_translation():
        print("Kısayol yakalandı! Ekran görüntüsü alma ve OCR işlemi başlatılıyor...")

triggerr = VisualBased()
triggerr.start()