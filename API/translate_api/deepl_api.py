import deepl
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import *
from actions.func_main import get_conf_api_json, json_read,get_current_api, write_file, get_save_location
from actions.copylisten import CopyListen
from actions.msgbox import ReturnErr
from actions.popup import TranslationPopup

class DeeplAPI(QThread):
    def __init__(self):
        super().__init__()
        
        self.auth_key = get_current_api()
        self.save_loc = get_save_location()
        
        
        self.translator = deepl.Translator(self.auth_key)
        
        self.worker = CopyListen()
        self.worker.link_found.connect(self.word_found)
        self.worker.start()
        
        self.popup = TranslationPopup()
        
    
    def start(self):
        self.worker.start()
    
    def stop(self):
        self.worker.stop()
    
    def word_found(self, word):
        try:
            translated = self.translator.translate_text(word, target_lang="TR").text
            full_translate = f"{word} | {translated}\n"
            self.popup.show_at_cursor(translated)
            
            write_file(self.save_loc, full_translate)
            
        except Exception as e:
            err_msgboc = ReturnErr(e)
            err_msgboc.exec()
    