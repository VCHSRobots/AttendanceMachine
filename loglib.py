#! /usr/bin/python
# ---------------------------------------------------------------------
# loglib.py -- Functions that deal with the log.
#
# created 1/1/15 DLB
# ---------------------------------------------------------------------

# These functions deal with log data... 

import os
import time
import csv

os.environ["TZ"] = "America/Los_Angeles"

# ---------------------------------------------------------------------
# Returns the time as a string in a format suitable for the log.
# ALL times are recorded as local to Los Angeles.
def GetLogTime() :
    t = time.localtime(time.time())
    return time.strftime("%Y/%m/%d %H:%M:%S", t)

# ---------------------------------------------------------------------
# Checks if time is a reasonable value... True if okay, false 
# otherwize.
def TimeOkay() :
    t = time.localtime(time.time())
    if(t.tm_year < 2015) : return False
    return True

# --------------------------------------------------------------------
# Gets current log file name.  Files change by date.
def LogFileName() :
    t = time.localtime(time.time())
    name = "jsonlogs/log_%4d_%02d_%02d" % (t.tm_year, t.tm_mon, t.tm_mday)
    return name

# --------------------------------------------------------------------
# Records a scan
#def RecordScan(badgeID, Side, Flags, LastName, FirstName) :
#    filename = LogFileName()
#    file = open(filename, "a")
#    tm = GetLogTime();
#  line = '= ' + tm + ', ' + badgeID + ', ' + Side + ', ' + Flags + ', ' + LastName + ', ' + FirstName + "\n"
#   file.write(line)
#   file.close()
    
# --------------------------------------------------------------------
# Records a scan (JSON)
def RecordScanJSON(parsed_json) :
    filename = LogFileName()
    file = open(filename, "a")
    tm = GetLogTime()
    file.write(parsed_json)
    file.close()
	

# ---------------------------------------------------------------------
# Records a message
def RecordMsg(msg) :
    filename = LogFileName()
    file = open(filename, "a")
    tm = GetLogTime();
    line = '* ' + tm + '> ' + msg + "\n"
    file.write(line)
    file.close()
