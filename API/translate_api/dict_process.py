import requests
from typing import Dict, List

API_KEY = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def get_word_dict_info(word: str):
    word_dict: List[Dict] = []
    
    full_word = API_KEY + word
    
    #Sunucuya istek atar
    response = requests.get(full_word)
    
    if response.status_code == 200:
        result = response.json()
    else:
        return response.status_code
    
    #İstenilen bilgileri alır (type, example, audio)
    try:
        phonetics = result[0].get("phonetics", [])
        
        for phone in phonetics:
            if phone.get("audio"): 
                audio_url = phone.get("audio")
                break
            
        if audio_url:
            word_dict.append({"audio": audio_url})
            
    except Exception as e:
        return e
        
    return word_dict
