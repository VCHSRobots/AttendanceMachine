#Imports
import json
import socket
from loglib import *
#Functions
def AddToQue(badgeid, side, flags, lastname, firstname): 
    tm = GetLogTime();
    json_string = '{"logtime": "' + tm + '", "badgeid": "' + badgeid + '", "side": "' + side + '", "flags": "' + flags + '", "lastname": "' + lastname + '", "firstname": "' + firstname +'"}'
    RecordScanJSON(json_string + "\r\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ("epicarg.xyz", 3265)
    s.sendto(json_string, address)
    s.close() 
    return
