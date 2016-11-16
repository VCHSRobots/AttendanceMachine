# -*- coding: utf-8 -*- Compiled with Python version 2.7.9 by TastyDucks
import socket, time, select, requests
from multiprocessing import Process
####################
#  Check CMD Code  #
####################
CONNECTION_LIST = []
def broadcast_data(sock, message):
	if message == "!":
		return
	else:
		length = len(message)
		message = "<" + str(length) + ">" + message
		for socket in CONNECTION_LIST:
			if socket != server_socket:
				try:
					socket.send(message)
					log("[INFO] ///Broadcast/// message: " + message + ": Sent to client (%s, %s)" %addr + " at " + CurrentTime + "<br>")
				except Exception,e: print str(e)
				except:
					log("[WARN] Failed to send ///Broadcast/// message to client (%s, %s)" %addr + ": Removing from client list")
					socket.close()
					CONNECTION_LIST.remove(socket)
def log(msg):
	print(msg)
	with open("outlog.txt", "a") as file:
		file.write(msg + "\n")
cmd = "null"
log("[INFO] CheckCmd script started.")
def CheckCmd():
	while True:
		CurrentTime = time.strftime("%Y/%m/%d-%H:%M:%S")
		with open("ConList.txt", "r") as file:
			CONNECTION_LIST = file.readlines()
		cmd="!"
		with open("cmd.txt", "rw+") as file:
			for cmd in file:
				cmd=cmd.strip()
				file.truncate(0)
				read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])
				for sock in read_sockets:
					if cmd == "rqln":
						broadcast_data(sock, "rqln")
						log("[INFO] ///RQLN/// Command recieved at : " + CurrentTime + "<br>")
						return
					elif cmd == "rqla":
						broadcast_data(sock, "rqla")
						log("[INFO] ///RQLA/// Command recieved at : " + CurrentTime + "<br>") 
						return
					elif cmd == "rqlo":
						broadcast_data(sock, "rqlo")
						log("[INFO] ///RQLO/// Command recieved at : " + CurrentTime + "<br>")
						return
					elif cmd == "rqul":
						broadcast_data(sock, "rqul")
						log("[INFO] ///RQUL/// Command recieved at : " + CurrentTime + "<br>")
						return
					elif cmd == "psul":
						broadcast_data(sock, "psul")
						log("[INFO] ///PSUL/// Command recieved at : " + CurrentTime + "<br>")
						return
					elif cmd == "tgdm":
						broadcast_data(sock, "tgdm")
						log("[INFO] ///TGDM/// Command recieved at : " + CurrentTime + "<br>")
						return
					else:
						print("[FATL] Error reading file cmd.txt at : " + CurrentTime + "<br>")
						return
CheckCmd()
