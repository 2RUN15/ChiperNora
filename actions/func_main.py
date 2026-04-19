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
            data = json.load(f)
        return data
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