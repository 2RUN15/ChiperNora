import deepl
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import *
from actions.func_main import (
    get_conf_api_json,
    json_read, get_current_api,
    write_file,
    get_save_location,
    get_datetime_today,
    path_join,
    check_is_folder,
    get_active_engine)
from actions.copylisten import CopyListen
from actions.msgbox import ReturnErr, ReturnErr_Ok_No
from actions.popup import TranslationPopup
import requests
from API.translate_api.dict_process import get_word_dict_info
from actions.bashscripts import bash_wget
import os
from datapack import WirteFilePack

DATE_TODAY = get_datetime_today()

class TranslateAPI(QObject):
    def __init__(self):
        super().__init__()
        
        self.auth_key = get_current_api()
        self.save_loc = get_save_location()
        self.active_engine = get_active_engine()
        
        if self.active_engine == "google":   
            self.url = f"https://translation.googleapis.com/language/translate/v2?key={self.auth_key}"
            self.payload = {
                "q": [],
                "target": "tr",
                "source": "en"
            }

        elif self.active_engine == "deepl":
            self.url = "https://api-free.deepl.com/v2/translate"
            self.payload = {
                "text": [],
                "target_lang": "TR",
                "source_lang": "EN",
                "formality": "default"
            }
            self.headers = {
                "Authorization": f"DeepL-Auth-Key {self.auth_key}",
                "Content-Type": "application/json"
            }        
        
        self.save_folder = path_join([os.path.dirname(self.save_loc),"attachments"])
        check_is_folder(self.save_folder)
        
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
        self.active_engine = get_active_engine()
    
    def word_found(self, word):
        #Kelimeyi çevirir
        try:
            if self.active_engine == "deepl":
                translated = self.translate_deepl(word)
            elif self.active_engine == "google":
                translated = self.translate_google(word)
            
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
                packs.boolValue = True
                write_file(packs)
            
        except Exception as e:
            err_msgboc = ReturnErr(e)
            err_msgboc.exec()
    
    def translate_deepl(self, word: str) -> str:
        self.payload["text"] = [word]
        response = requests.post(self.url, json=self.payload,headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            translated = response_json["translations"][0]["text"]
            
            return translated
    
    def translate_google(self, word: str) -> str:
        self.payload["q"] = [word]
        response = requests.post(self.url, json=self.payload)
        if response.status_code == 200:
            response_json = response.json()
            translated = response_json["data"]["translations"][0]["translatedText"]
            
            return translated
        