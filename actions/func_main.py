import json
import os
from datetime import datetime
from API.translate_api.dict_process import get_word_dict_info
from actions.bashscripts import bash_wget
from datapack import WirteFilePack
import platform

MAIN_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(MAIN_PATH)

MD_SCHEME = """
| Kelime     | Tür   | Anlamı                     | Örnek Cümle                                | Okunuşu |
| :--------- | :---- | :------------------------- | :----------------------------------------- | :------- |
"""

#Json dosyasını kaydeder
def json_save(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=True)
    except Exception as e:
        raise e

#Json dosyasını okur
def json_read(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise e

#Dosya okur
def file_read(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file = f.read()
        return file
    except Exception as e:
        raise e

#Base çalışma klasörünün yolunu döndürür
def get_base_dir():
    try:
        return os.path.join(BASE_DIR, os.pardir)
    except Exception as e:
        raise e

#Base klasörüne ekleme yapar
def path_join(file_paths: list):
    try:
        base_dir = get_base_dir()
        full_path = os.path.join(base_dir, *file_paths)
        return full_path
    except Exception as e:
        raise e

#API Json dosyasını alır
def get_conf_api_json():
    try:
        file_path = path_join(["API","config.json"])
        return file_path
    except Exception as e:
        raise e

#Aktif olan api engine alır
def get_active_engine():
    try:
        file_path = get_conf_api_json()
        file = json_read(file_path)
        engine = file["active_engine"]
        
        return engine
    except Exception as e:
        raise e

#Aktif olan api engine'nin api anahtarını alır
def get_current_api():
    try:
        active_engine = get_active_engine()
        file_path = get_conf_api_json()
        read_file = json_read(file_path)
        engines = read_file["engines"]
        
        if active_engine == "deepl":
            return engines["deepl"]["api_key"]
        elif active_engine == "google":
            return engines["google"]["api_key"]
        else:
            return engines["mymemory"]["email"]
    except Exception as e:
        raise e 

#İlk defa açılıp açılmadığını kontrol eder
def get_first_open():
    try:
        file_path = get_conf_api_json()
        read_file = json_read(file_path)
        first_open = read_file["settings"]["first_open"]
        
        return first_open
    except Exception as e:
        raise e

#Kaydetme konumunu alır
def get_save_location():
    try:
        file_path = get_conf_api_json()
        read_file = json_read(file_path)
        
        return read_file["settings"]["save_file"]
    except Exception as e:
        raise e

#Varsayılan ayarları sıfırlar
def create_conf_json(default: bool):
    try:
        api_conf = {
            "active_engine": "deepl",
            "engines": {
                "deepl": {
                    "api_key": ""
                },
                "google": {
                    "api_key": ""
                },
                "mymemory": {
                    "email": ""
                }
            },
            "settings": {
                "save_file": "",
                "first_open": False,
                "word_limit": 1,
                "format": ""
            }
        }
        
        
        conf_path = path_join(["API","config.json"])
        if not os.path.isfile(conf_path) or default:
            json_save(conf_path, api_conf)
        else:
            return
    except Exception as e:
        raise e

#Md dosyasının düzenini oluşturur
def check_md_file(file_path):
    is_md_scheme = True
    
    with open(file_path, "r", encoding="utf-8") as f:
        for _ in range(10):
            line = f.readline()
            if line in MD_SCHEME:
                is_md_scheme = False
            if not line:
                break
    
    if is_md_scheme == False:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(MD_SCHEME)

#Klasörün var olup olmadığını kontrol eder
def check_is_folder(file_path: str):
    is_folder = os.path.isdir(file_path)
    
    if is_folder:
        return
    os.mkdir(file_path)

#Md dosyasına verileri yazar
def write_md_file (packs: WirteFilePack):
    save_loc = get_save_location()
    word = packs.full_word["word"]
    translated = packs.full_word["translated"]
    
    if packs.boolValue == True:
        md_format = f"|      {word}      |       |             {translated}               |                                            |    Bulunamadı     |\n"

    else:
        save_folder = path_join([os.path.dirname(save_loc),"attachments"])
        audio_link = packs.word_dict[0]["audio"]
        audio_name = audio_link.split("/")[-1]
        bash_wget(save_folder, audio_link)
        
        md_format = f"|      {word}      |       |             {translated}               |                                            |    ![[{audio_name}]]     |\n"
    
    with open(save_loc,"a",encoding="utf-8") as f:
        f.write(md_format)
    
#txt mi md mi olup olmadığını kontrol eder. Txt ise basit şekilde yazar
def write_file(packs: WirteFilePack):
    try:
        _,extention = os.path.splitext(packs.file_path)
        if extention == ".txt":
            full_translated = f"{packs.full_word["word"]} | {packs.full_word["translated"]}\n"
            with open (packs.file_path, "a", encoding="utf-8") as f:
                f.write(full_translated)
        elif extention == ".md":
            write_md_file(packs)
    except Exception as e:
        raise e

#Bugünün tarihini (Yıl-Ay-Gün) olacak şekilde alır
def get_datetime_today():
    today = datetime.today()
    date = f"{today.year}-{today.month}-{today.day}"
    return date