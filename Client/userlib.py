#! /usr/bin/python
# ---------------------------------------------------------------------
# userlib.py -- Functions that deal with users.
#
# created 1/1/15 DLB
# ---------------------------------------------------------------------

# These functions deal with user data... 

import csv

# ---------------------------------------------------------------------
# Dies with message on programming errors.
def DieWithMsg(msg) :
    print("Error!  Quiting Program. \n")
    print(msg + "\n")
    exit()

# ---------------------------------------------------------------------
# Class to hold the user data.
class UserData :
    firstname = ""
    lastname  = ""
    badgeid   = ""
    picfile   = ""

# ---------------------------------------------------------------------
# finds the key in a header line.  The header is a list
# of captions from the csv file.  The index of the column
# is returned.
def findkey(header, v) :
    i = 0;
    for k in header :
        if v == k : return i
        i += 1
    return -1

# ---------------------------------------------------------------------
# Reads the users file, returns an array of users.  Dies if the 
# input file is not properly formatted.
def GetUsers() :
    users = []
    try:
        with open('UserList.csv') as csvfile:
            crd = csv.reader(csvfile)
            n = 0;
            for row in crd:
                if(n == 0) :
                    header = row
                    username = findkey(row, "UserName")
                    firstname = findkey(row, "FirstName")
                    lastname  = findkey(row, "LastName")
                    badgeid   = findkey(row, "BadgeID")
                    picfile   = findkey(row, "Picture")
                    if(username < 0 or firstname < 0 or lastname < 0 or badgeid < 0) :
                         DieWithMsg("Bad Header in userlist.csv")
                else :
                    d = UserData();
                    d.firstname = row[firstname]
                    d.lastname  = row[lastname]
                    d.badgeid   = row[badgeid]
                    d.picfile   = row[picfile]
                    users.append(d)
                n += 1
            return users;    
    except Exception :
        return users;

# ---------------------------------------------------------------------
# Given an array of user objects returns the one with the badgeid. 
# Returns False if not found.
def FindUser(users, badgeid) :
     for u in users :
         if(u.badgeid.lower() == badgeid.lower()) : return u
     return False     

