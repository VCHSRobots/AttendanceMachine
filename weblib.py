# -*- coding: utf-8 -*-
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
    data = "SCAN:" + json_string
    BroadcastData(data)
    return
def PushNewestLogToServer():
    newestlog = max(glob.iglob(os.path.join("logs/", "*")), key=os.path.getctime)
    with open(newestlog, "r") as file:
        data = "LOGN:" + file.read()
        BroadcastData(data)
    return
def PushAllLogsToServer():
    data = ""
    FullData = ""
    FileList = os.listdir("logs/")
    for filename in FileList:
        with open("logs/" + filename, "r") as file:
            pdata = file.read()
            data += pdata + "%"
    data = "LOGA:" + data
    BroadcastData(data)
    return
def PushUserlistToServer():
    with open("UserList.csv", "r") as file:
        data = "USRL:" + file.read()
        BroadcastData(data)
def BroadcastData(data):
    length = len(data)
    fdata = "<" + str(length) + ">" + data
    s.send(fdata)
def CommMan():
    while True:
        data = s.recv(16)
        if data != "":
            if data[0] == "<":
                EOH = False
                mlength = ""
                hlength = 1
                for char in data[1:]:
                   if char == ">":
                       hlength += 1
                       break
                   else:
                       mlength += char
                       hlength += 1
                       MessageLength = int(mlength)
                       RecvLength = 0 - hlength
                       message = ""
                       message += data
                       RecvLength += len(data)
                       if RecvLength >= MessageLength:
                           message = message.split('>', 1)[-1]
                           if message == "rqln":
                               PushNewestLogToServer()
                           elif message == "rqla":
                               PushAllLogsToServer()
                           elif message == "rqul":
                               PushUserlistToServer()
                           elif message == "tgdm":
                               print "Toggling demo video... Note: this does not do anything at the moment."
                       else:
                           continue
            else:
                print "[WARN] Major Server Error! Server not giving proper data headers!"
        else:
            print "[WARN] Server appears to have gone offline!"
