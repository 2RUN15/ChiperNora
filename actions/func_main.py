import json
import os

MAIN_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(MAIN_PATH)

def json_save(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=True)
    except Exception as e:
        raise e

def json_read(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise e

def file_read(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file = f.read()
        return file
    except Exception as e:
        raise e

def get_base_dir():
    try:
        return os.path.join(BASE_DIR, os.pardir)
    except Exception as e:
        raise e

def path_join(file_paths: list):
    try:
        base_dir = get_base_dir()
        full_path = os.path.join(base_dir, *file_paths)
        return full_path
    except Exception as e:
        raise e
    
def get_conf_api_json():
    try:
        file_path = path_join(["API","config.json"])
        return file_path
    except Exception as e:
        raise e

def get_active_engine():
    try:
        file_path = get_conf_api_json()
        file = json_read(file_path)
        engine = file["active_engine"]
        
        return engine
    except Exception as e:
        raise e

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
        
        return 
    except Exception as e:
        raise e 

def get_save_location():
    try:
        file_path = get_conf_api_json()
        read_file = json_read(file_path)
        
        return read_file["settings"]["save_file"]
    except Exception as e:
        raise e

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
                "word_limit": 1
            }
        }
        
        
        conf_path = path_join(["API","config.json"])
        if not os.path.isfile(conf_path) or default:
            json_save(conf_path, api_conf)
        else:
            return
    except Exception as e:
        raise e

def write_file(file_path: str, full_word: str):
    try:
        with open (file_path, "a", encoding="utf-8") as f:
            f.write(full_word)
    except Exception as e:
        raise e