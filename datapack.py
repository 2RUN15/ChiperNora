from dataclasses import dataclass

@dataclass
class warningmsg:
    window_tittle: str
    text: str

@dataclass
class WirteFilePack:
    file_path: str
    full_word: str
    date_today: str
    word_dict: int | str
    boolValue: bool | None