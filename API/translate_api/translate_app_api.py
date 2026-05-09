import deepl
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import *
from actions.func_main import get_conf_api_json, json_read, get_current_api, write_file, get_save_location, get_datetime_today, path_join,check_is_folder
from actions.copylisten import CopyListen
from actions.msgbox import ReturnErr, ReturnErr_Ok_No
from actions.popup import TranslationPopup
import requests
from API.translate_api.dict_process import get_word_dict_info
from actions.bashscripts import bash_wget
import os
from datapack import WirteFilePack

DATE_TODAY = get_datetime_today()

class DeeplAPI(QObject):
    def __init__(self):
        super().__init__()
        
        self.auth_key = get_current_api()
        self.save_loc = get_save_location()
        self.save_folder = path_join([os.path.dirname(self.save_loc),"attachments"])
        check_is_folder(self.save_folder)
        
        self.translator = deepl.Translator(self.auth_key)
        
        #Kopyalanan sözcükleri dinleme
        self.worker = CopyListen()
        self.worker.link_found.connect(self.word_found)
        self.worker.start()
        
        self.popup = TranslationPopup()
    
    def start(self):
        self.worker.start()
    
    def stop(self):
        self.worker.stop()

    def update_settings(self):
        #Ayarları günceller
        self.auth_key = get_current_api()
        self.save_loc = get_save_location()
    
    def word_found(self, word):
        #Kelimeyi çevirir
        try:
            translated = self.translator.translate_text(word, target_lang="TR").text
            full_translated = {"word": word, "translated": translated}
            self.popup.show_at_cursor(translated)
            
            word_dict = get_word_dict_info(word)
            
            if word_dict == 404:
                return
            
            packs = WirteFilePack(
                file_path=self.save_loc,
                full_word=full_translated,
                date_today=DATE_TODAY,
                word_dict= word_dict,
                boolValue=None
            )

            #Dosyaya yazar
            write_file(packs)

        except TypeError:
            err_msg = "Sözlükte böyle bir kelime bulunamadı.\nKelimeyi sözlüğe eklemek ister misiniz ?"
            err_msgbox = ReturnErr_Ok_No(err_msg)
            err_msgbox.exec()
            
            clicked = err_msgbox.clickedButton()
            
            if err_msgbox.standardButton(clicked) == QMessageBox.StandardButton.Yes:
                print("Burada")
                packs.boolValue = True
                write_file(packs)
            
        except Exception as e:
            err_msgboc = ReturnErr(e)
            err_msgboc.exec()
        

class GoogleAPI(QObject):
    def __init__(self):
        super().__init__()
        
        self.auth_key = get_current_api()
        self.save_loc = get_save_location()
        
        self.is_activate = True
        
        self.popup = TranslationPopup()
        
        self.url = "https://translation.googleapis.com/language/translate/v2"
        self.payload = {
            "key": self.auth_key,
            "q": "",
            "target": "tr",
            "source": "en"
        }
        
        self.worker = CopyListen()
        self.worker.link_found.connect(self.word_found)
        self.worker.start()
    
    def start(self):
        if not self.is_activate:
            self.worker.start()
            self.is_activate = True
    
    def stop(self):
        if self.is_activate:
            self.worker.stop()
            self.is_activate = False
    
    def update_settings(self):
        self.auth_key = get_current_api()
        self.save_loc = get_save_location()
    
    def word_found(self, word):
        try:
            self.payload["q"] = word
            
            response = requests.post(self.url, self.payload)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result["data"]["translations"][0]["translatedText"]
                self.popup.show_at_cursor(translated_text)
                
                full_translate = f"Google | {word} | {translated_text}\n"
                
                write_file(self.save_loc, full_translate)
            else:
                err_msgbox = ReturnErr(response.text)
                err_msgbox.exec()
        
        except Exception as e:
            err_msgbox = ReturnErr(e)
            err_msgbox.exec()