#------------------------
#Imports
#------------------------
import json
import threading
import socket
import glob
from loglib import *
#------------------------
#Global Variables
#------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("epicarg.xyz", 3265))
#------------------------
#Functions
#------------------------
def CommunicationsManager():
    return
def PushScanToServer(badgeid, side, flags, lastname, firstname): 
    tm = GetLogTime()
    json_string = '{"logtime": "' + tm + '", "badgeid": "' + badgeid + '", "side": "' + side + '", "flags": "' + flags + '", "lastname": "' + lastname + '", "firstname": "' + firstname +'"}'
    RecordScanJSON(json_string + "\r\n")
    data = "SCAN:" + json_string
    s.send(data)
    return
def PushNewestLogToServer():
    newestlogs = min(glob.iglob("jsonlogs/*"), key=os.path.getctime)
    with open("newestlog", "r"):
        data = "LOGN:" + newestlog.read()
        s.send(data)
def PushAllLogsToServer():
    data = ""
    for filename in os.listedir(os.getcwd()):
        with open(filename, "r"):
            data += filename + "%"
    data = "LOGA:" + data
    s.send(data)
