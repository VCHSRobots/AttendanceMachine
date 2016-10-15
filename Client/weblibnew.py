# -*- coding: utf-8 -*-
#------------------------
#Imports
#------------------------
import json, threading, socket, glob, thread, time, sys
from loglib import *
#------------------------
#Global Variables
#------------------------
ConnToServer = False
que = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#------------------------
#Functions
#------------------------
def PushScanToServer(badgeid, side, flags, lastname, firstname): 
    tm = GetLogTime()
    json_string = '{"logtime": "' + tm + '", "badgeid": "' + badgeid + '", "side": "' + side + '", "flags": "' + flags + '", "lastname": "' + lastname + '", "firstname": "' + firstname +'"}'
    RecordScanJSON(json_string + "\r\n")
    data = "SCAN:" + json_string
    BroadcastData(data)
    print("returned from server?")
    return
def PushNewestLogToServer():
    newestlog = max(glob.iglob(os.path.join("scanlogs/", "*")), key=os.path.getctime)
    with open(newestlog, "r") as file:
        data = "LOGN:" + file.read()
	print("data sending:"+data)
        BroadcastData(data)
    return
def PushAllLogsToServer():
    data = ""
    FullData = ""
    FileList = os.listdir("scanlogs/")
    for filename in FileList:
        with open("scanlogs/" + filename, "r") as file:
            pdata = file.read()
            data += pdata + "%"
    data = "LOGA:" + data
    BroadcastData(data)
    return
def PushUserlistToServer(data):
    with open("UserList.csv", "r") as file:
        data = "USRL:" + file.read(data)
def PullUserListFromServer():
    with open("UserList.csv", "w") as file:
        data = "USRL:" + file.write(data)
def PushOutlogToServer():
    with open("outlog", "r") as file:
        data = "LOGO:" + file.read()
        BroadcastData(data)
def BroadcastData(data):
    global ConnToServer
    length = len(data)
    fdata = "<" + str(length) + ">" + data
    if ConnToServer == True:
        s.send(fdata)
	print("data sent"+fdata)
    else:
        AddToQue(fdata)
def AddToQue(data):
    global que
    que.append(data)
def ConnectToServer():
    global ConnToServer
    global que
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
	server="104.236.140.24"
	port=3265
        s.connect((server, port))
        ConnToServer = True
        RecordMsg("[INFO] Connected to remote server.")
        if que != []:
            i = 0
            time.sleep(1)
            for scan in que:
                s.send(scan)
                i += 1
                sys.stdout.write("\r[INFO] %d" % i + " of " + str(len(que)) + " backlog scans sent to server")
                sys.stdout.flush()
                time.sleep(0.25)
            sys.stdout.write("\r")
            sys.stdout.flush()
            RecordMsg("[INFO] All backlog scans sent to server : " + str(len(que)) + " items; " + str(len("".join(que))) + " bits")
            que = []
    except Exception as e:
        RecordMsg("[FATL] Unable to connect to server" + server +" : " + str(e))
        ConnToServer = False
        RecordMsg("[INFO] Attempting to reconnect to the server in 10 seconds...")
        time.sleep(10)
        ConnectToServer()
def CommMan():
    print("CommMan running")
    global ConnToServer
    global s
    ConnectToServer()
    while ConnToServer == True:
        print("in connected to server while loop here")
	data = s.recv(16)
        if data != "":
	    print("Message received")
            print(data)
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
                           print("message:"+message)
			   message = message.split('>', 1)[-1]
                           if message == "rqln":
                               PushNewestLogToServer()
                           elif message == "rqla":
                               PushAllLogsToServer()
                           elif message == "rqlo":
                               PushOutlogToServer()
                           elif message == "rqul":				
                               PushUserlistToServer()
                           elif message == "tgdm":
                               RecordMsg("[INFO] Toggling demo video... Note: This does NOT do anything at the moment.")
                       else:
                           continue
            else:
                RecordMsg("[WARN] Server not giving proper data headers.")
        else:
            RecordMsg("[FATL] Server appears to have gone offline.")
            ConnToServer = False
    ConnectToServer()
