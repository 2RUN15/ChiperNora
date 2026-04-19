def change_engine(cmb_engine):
    if cmb_engine == 0:
        text = "mymemory"
    elif cmb_engine == 1:
        text = "deepl"
    elif cmb_engine == 2:
        text = "google"
    
    return text

def re_change_engine(cmb_engine):
    if cmb_engine == "mymemory":
        cur_in = 0
    elif cmb_engine == "deepl":
        cur_in = 1
    elif cmb_engine == "google":
        cur_in = 2
    
    return cur_in