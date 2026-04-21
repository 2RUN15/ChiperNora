from actions.msgbox import *
from datapack import warningmsg

def warn_api_key():
    warninmess_data = warningmsg(
        window_tittle="EMPTY API",
        text="Please make sure you enter your API key."
    )
    warningmsg_win = WarningMess(warninmess_data)
    warningmsg_win.exec()

def warn_save_loc():
    warninmess_data = warningmsg(
        window_tittle="Choose Save Location",
        text="Save location not choosed"
    )
    warningmsg_win = WarningMess(warninmess_data)
    warningmsg_win.exec()