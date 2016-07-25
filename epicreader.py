#! /usr/bin/python
# ---------------------------------------------------------------------
# epicreader.py -- Main attandence reading application for Epic Robotz.
#
# created 1/1/15 DLB
# ---------------------------------------------------------------------

# This program was developed for Epic Robotz to take attendance 
# with a bar code reader.
# 
# This program is intended to run on a Rasberry Pi, without ever
# stopping.  On each barcode scan, it determins who make the
# scan, displays their picture, and then writes data about the
# scan to the log file.  After 15 seconds, the picture is
# removed, and the screen goes dark.
#
# 
#

import socket
import Tkinter
import tkMessageBox
import tkFont
import os.path
import os
import string
from loglib import *      # Routines to log to a file
from userlib import *     # Routines that deal with users
from weblib import *	  # Routines that deal with uploding scan data to webserver

# ---------------------------------------------------------------------
# Define global variables...
users     = []  #array of users, each with badgeid.
nscans    = 0   #number of scans since program invoke
nbadscans = 0   #number of unknown, bad scans.
nnotexist = 0   #number of scans where someone didn't exist
sx        = 0   #size of screen, in x
sy        = 0   #size of screen, in y
flags  = "okay" #system flags.
cleanmode = True
secs_to_clear = 0  #number of seconds before clearing scan data from screen
ipaddr = "??"; 

# ---------------------------------------------------------------------
def GetIPAddr() :
    global ipaddr
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        ipaddr = s.getsockname()[0]
        s.close()
    except Exception :
        ipaddr ="?exception?"    
        
# ---------------------------------------------------------------------
# Shows the status
def ShowStatus() :
    if(cleanmode) : s = ""
    else          : 
        s = 'Time=' + GetLogTime()
        s += ', Scans=' + str(nscans)
        s += ', BadScns=' + str(nbadscans)
        s += ', ?ID=' + str(nnotexist)
        s += ', IP=' + ipaddr
    c.itemconfigure(tx_status, text=s)
    if(TimeOkay() == False) : s = "Bad\nTime!"
    else                    : s = ""
    c.itemconfigure(tx_badtime, text=s)
    if(flags == 'okay') : s = ""
    else : s = flags
    c.itemconfigure(tx_flags, text=s)
    
# ---------------------------------------------------------------------
# Shows the scan line, if not cleanmode.
def ShowScan(line) :
    if(cleanmode) : c.itemconfigure(tx_scan, text="");    #!! for debug.
    else          : c.itemconfigure(tx_scan, text=line);

# ---------------------------------------------------------------------
# Builds line from input key presses.  Actually the key presses is
# normally the barcode reader.
input_line = '';
def CharInput(event) :
    global input_line;
    if(event.keysym == "Escape") : exit();
    if(event.keysym == "KP_Enter" or event.keysym == "Return") :
        ProcessInput(input_line);
        input_line = "";
    else :
        input_line += event.char

# ---------------------------------------------------------------------
# Analyze Scan data, returns false on failure, or a tuple of 
# (prefix, badgeid, side) prefix is whatever is found.
# badgeid is in form A000, and side is either 'front' or 'back'.

def AnalyzeScan(line) :
    line = line.strip()
    if(len(line) <=0) : return False
    if(string.find(string.letters + string.digits, line[0]) < 0) : return False
    if(string.find(string.letters + string.digits, line[1]) < 0) : return False
    prefix = line[0:1]
    if(line[2] != ' ') : return False
    if(string.find(string.letters, line[3]) < 0) : return False
    if(string.find(string.digits, line[4]) < 0) : return False
    if(string.find(string.digits, line[5]) < 0) : return False
    if(string.find(string.digits, line[6]) < 0) : return False
    if(line[7].lower() == 'f') : side = 'front'
    elif (line[7].lower() == 'b') : side = 'back'
    else : return False
    badgeid = line[3:7];
    return (prefix, badgeid, side)

# ---------------------------------------------------------------------
# Show picture, if there is one... otherwise, blank
def ShowPic(badgeid) : 
    global img
    filename = 'gifs/' + badgeid.upper() + '.gif';
    if(not os.path.exists(filename)) :
       c.itemconfigure(tx_img, state=Tkinter.HIDDEN)
       return
    img = Tkinter.PhotoImage(file=filename);
    c.itemconfigure(tx_img, image=img,  state=Tkinter.DISABLED)
    return

def ClearScan() :
    c.itemconfigure(tx_img, state=Tkinter.HIDDEN)
    c.itemconfigure(tx_black, state=Tkinter.HIDDEN)
    c.itemconfigure(tx_name, text="")
    c.itemconfigure(tx_rect, fill="#FFFFFF")
    c.itemconfigure(tx_announce, text="", fill="#00FFFF");
    c.itemconfigure(tx_scan, text="");
    
# ---------------------------------------------------------------------
# Process input... look for badge scans or commands.  Everything gets
# logged.    
def ProcessInput(line) :
    global nscans, flags, cleanmode, secs_to_clear, nbadscans, nnotexist

    nscans += 1
    c.itemconfigure(tx_black, state=Tkinter.HIDDEN)
    ShowStatus()
    ShowScan(line)
    if(line.lower().strip() == 'exit') : 
        exit()
    if(line.lower().strip() == 'test') :
        if(flags == 'test') : flags = 'okay'
        else : flags = 'test'
        ShowStatus()
        return
    if(line.lower().strip() == 'reset') :
        flags = 'okay'
        GetIPAddr()
        cleanmode = True
        ClearScan()
        ShowScan(line)
        ShowStatus()
        return
    if(line.lower().strip() == 'verbose' or line.lower().strip() == 'status') :
        if(cleanmode == True) : cleanmode = False
        else : cleanmode = True
        ShowScan(line)
        ShowStatus()
        return
    if(line.lower().strip() == 'sleep') :
        c.itemconfigure(tx_black, state=Tkinter.DISABLED)
        return
    
    # The scan was not a command... 
    ClearScan()
    ShowScan(line)
    scandata = AnalyzeScan(line)
    secs_to_clear = 5
    if(scandata == False) :
        RecordMsg("Bad Scan: " + line)
        c.itemconfigure(tx_rect, fill="#FF0000")
        c.itemconfigure(tx_announce, text="Bad Scan", fill="#00FFFF");
        nbadscans += 1
        ShowStatus()
        return
    badgeid = scandata[1]
    side    = scandata[2]
    user = FindUser(users, badgeid)
    if(user != False) :
        c.itemconfigure(tx_name, text=user.firstname + " " + user.lastname)
        lastname = user.lastname
        firstname = user.firstname
    else :
        c.itemconfigure(tx_name, text="")
        lastname = ""
        firstname = ""
        nnotexist += 1
    ShowStatus()
    ShowPic(badgeid)
    AddToQue(badgeid, side, flags, lastname, firstname)
    user = (badgeid, side, "pic1.gif")
    #ShowPic(user)
    if(side == 'front') :
        c.itemconfigure(tx_rect, fill="#00FF00")
        c.itemconfigure(tx_announce, text="Welcome", fill="#000000");
        return
    if(side == 'back') :
        c.itemconfigure(tx_rect, fill="#0000FF")
        c.itemconfigure(tx_announce, text="Goodbye", fill="#FFFF00");
        return

# ---------------------------------------------------------------------
# Called once per second.  Used for dynamic updating of screen.
seccounter = 0;
def SecEvent() :
    global seccounter, secs_to_clear
    root.after(1000, SecEvent)  #schedule next sec
    seccounter += 1
    #c.itemconfigure(tx_sec, text=str(seccounter))
    if(secs_to_clear > 0) :
        secs_to_clear -= 1
        if(secs_to_clear == 0) : ClearScan()
        
    
        
# ---------------------------------------------------------------------
# Mainline code starts here...

# Make sure our working directory is where the python script is.
p = os.path.dirname(os.path.realpath(__file__))
print p
os.chdir(p)

users = GetUsers()
nusers = len(users)

#Testing AnalyzeScan
#def Try(line) :
#    print line + " => ", AnalyzeScan(line)
#Try("aexa123xcr")
#Try("ae a123xcr")
#Try("ae a123x")
#Try("ae a123b")
#Try("ae a123f")
#Try("ae a1x3f")
#Try("ae 1a23f")

#Testing Log Functions...
#print "Number of members = " + str((len(users)))
#print "GetLogTime = " + GetLogTime()
#print "Is Time OKAY? = " + str(TimeOkay())
#print "LogFileName = " + LogFileName()
#RecordScan("A001f", "Brandon", "Dalbert")
#RecordMsg("Error: Unable to get time")

root = Tkinter.Tk()
root.title("Epic Robotz Attendance Reader");
sx = root.winfo_screenwidth() - 10;
sy = root.winfo_screenheight() - 50;
#sx = 1010;
#sy = 600;
s = "%dx%d+%d+%d" % (sx, sy, 0, 0);
root.geometry(s);

font_big   = tkFont.Font(family='Helvetica',size=65, weight='bold');
font_med   = tkFont.Font(family='Helvetica',size=40, weight='bold');
font_small = tkFont.Font(family='Helvetica',size=20, weight='bold');
font_tiny  = tkFont.Font(family='Helvetica',size=16, weight='bold');

c = Tkinter.Canvas(root, takefocus=1);
c.place(x=0, y=0, width=sx, height=sy);

tx_title = c.create_text(sx/2,0, text="ATTENDANCE READER",
    fill="#FF0000", font=font_med, state=Tkinter.DISABLED, anchor=Tkinter.N);

tx_rect = c.create_rectangle(0, 80, sx, 180, fill="#FFFFFF")

tx_announce = c.create_text(sx/2, 178, text="", fill="#000000", font=font_big,
    state=Tkinter.DISABLED, anchor=Tkinter.S)

tx_flags = c.create_text(0, sy-10, text="", fill="#FF0000", font=font_med,
    state=Tkinter.DISABLED, anchor=Tkinter.SW)
    
tx_name = c.create_text(sx/2, 470, text="", fill="#000000", font=font_med,
    state=Tkinter.DISABLED, anchor=Tkinter.N)

tx_scan = c.create_text(sx/2, 520, text="", fill="#000000", font=font_small,
    state=Tkinter.DISABLED, anchor=Tkinter.N);
    
tx_status = c.create_text(sx/2, 550, text="", fill="#000000", font=font_tiny, 
    state=Tkinter.DISABLED, anchor=Tkinter.N);
    
tx_badtime = c.create_text(10, sy/2, text="", fill="#FF0000", font=font_med,
    state=Tkinter.DISABLED, anchor=Tkinter.W)

tx_sec = c.create_text(sx-10, sy/2, text="", fill="#000000", font=font_small,
    state=Tkinter.DISABLED, anchor=Tkinter.E)
    
tx_users = c.create_text(sx, 0, text=str(nusers), state=Tkinter.DISABLED, anchor=Tkinter.SE)
   
tx_black = c.create_rectangle(0, 0, sx, sy, fill="#000000", state=Tkinter.HIDDEN)   
    
img = Tkinter.PhotoImage(file="startup.gif");
tx_img = c.create_image(sx/2, 190, image=img, anchor=Tkinter.N, state=Tkinter.DISABLED)
    
ShowStatus()
secs_to_clear = 20
GetIPAddr()
    
root.bind('<Any-Key>', CharInput)
root.after(1000, SecEvent)
root.mainloop()

#for u in users :
#    print(u.firstname + " " + u.lastname + " " + u.badgeid + "\n")



