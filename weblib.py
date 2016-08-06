#------------------------
#Imports
#------------------------
import json, threading, socket, glob, thread
from loglib import *
#------------------------
#Global Variables
#------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("epicarg.xyz", 3265))
#------------------------
#Functions
#------------------------
def PushScanToServer(badgeid, side, flags, lastname, firstname): 
    tm = GetLogTime()
    json_string = '{"logtime": "' + tm + '", "badgeid": "' + badgeid + '", "side": "' + side + '", "flags": "' + flags + '", "lastname": "' + lastname + '", "firstname": "' + firstname +'"}'
    RecordScanJSON(json_string + "\r\n")
    data = "SCAN:" + json_string + "^"
    s.send(data)
    return
def PushNewestLogToServer():
    newestlog = min(os.listdir("logs/"), key = os.path.getctime)
    with open("logs/" + newestlog, "r") as file:
        data = "LOGN:" + file.read() + "^"
        s.send(data)
    return
def PushAllLogsToServer():
    FullData = ""
    for filename in os.listdir(os.getcwd()):
        with open(filename, "r") as file:
            data = file.read()
            FullData += data + "%"
    FullData = "LOGA:" + FullData + "^"
    s.send(FullData)
    return
def PushUserlistToServer():
    with open("UserList.csv", "r") as file:
        data = "USRL:" + file.read() + "^"
        s.send(data)
def CommMan():
    while True:
        recvdata = s.recv(16)
          if recvdata[:4] == "rqln":
            PushNewestLogToServer()
        elif recvdata[:4] == "rqla":
            PushAllLogsToServer()
        elif recvdata[:4] == "rqul":
            PushUserlistToServer()
        elif recvdata[:4] == "tgdm":
            print "toggling demo video.... ;)"
