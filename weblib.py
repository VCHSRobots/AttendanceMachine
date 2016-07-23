import json
from loglib import *
def AddToQue(badgeid, side, flags, lastname, firstname): 
    tm = GetLogTime();
    json_string = '{"logtime": "' + tm + '", "badgeid": "' + badgeid + '", "side": "' + side + '", "flags": "' + flags + '", "lastname": "' + lastname + '", "firstname": "' + firstname +'"}'
    RecordScanJSON(json_string + "\r\n")
    return