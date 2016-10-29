# -*- coding: utf-8 -*- Compiled with Python version 2.7.9
#
# Running in background on Attendance Machine using command:
# nohup python scanner.py  &


import socket, time, select, threading, requests, thread
####################
# Main Server Code #
####################
if __name__ == "__main__":
	CONNECTION_LIST = []
	RECV_BUFFER = 64
	PORT = 3265
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(3)
	CONNECTION_LIST.append(server_socket)
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
		with open("/var/www/html/outlog.txt", "a") as file:
			file.write(msg + "\n")
	cmd = "null"
	class CheckCmdThread(threading.Thread):
		def __init__(self):
			super(CheckCmdThread, self).__init__()
		def run(self):
			while True:
				CurrentTime = time.strftime("%Y/%m/%d-%H:%M:%S")
				cmd="!"
			with open("/var/www/html/cmd.txt", "rw+") as file:
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
	log("[INFO] Attendance Server initiated on port " + str(PORT) + " at : " + time.strftime("%Y/%m/%d-%H:%M:%S") + "<br>")
	def DataTimeout():
		timeout = False
		#log("Timeout: Timer Started!")
		#time.sleep(6)
		#timeout = True
		#log("Timeout: Time's Up!")
	class CommManThread(threading.Thread):
		def __init__(self):
			super(CheckCmdThread, self).__init__()
		def run(self):
			message = ""
			EOH = False
			timeout = False
			RecvLength = 0
			MessageLength = 0
			while True:
				CurrentTime = time.strftime("%Y/%m/%d-%H:%M:%S")
				read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])
				for sock in read_sockets:
					if sock == server_socket:
						sockfd, addr = server_socket.accept()
						CONNECTION_LIST.append(sockfd)
						log("[INFO] Client (%s, %s) has connected" % addr + " at : " + CurrentTime  + "<br>")
					else:
						try:
		  					data = sock.recv(RECV_BUFFER)
							if data != "":
								try:
									if EOH == False:
										if data[0] == "<":
											mlength = ""
											hlength = 1
											for char in data[1:]:
												if char != ">":
													mlength += char
													hlength += 1
												else:
													hlength += 1
													MessageLength = int(mlength) + hlength
													EOH = True
										else:
											log("[WARN] ///Bad parse - No Start-Of-Header symbol/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + data + "<br>")
											message += data
											RecvLength += len(data)
											if timeout == False:
												if RecvLength == MessageLength:
													message = message.split('>', 1)[-1]
													RecvLength = 0
													MessageLength = 0
													EOH = False
													if message[:5] == "SCAN:":
														log("[INFO] ///Scan/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
														#requests.post('http://admin.epicscouts.org/reader_upload_scan.php', data = {'json':message[5:]})#data=message[5:])
														broadcast_data(sock, "!")
													elif message[:5] == "LOGN:":
														log("[INFO] ///Newest Scan Log/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
													elif message[:5] == "LOGA:":
														log("[INFO] ///All Scan Logs/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
													elif message[:5] == "LOGO:":
														log("[INFO] ///Out Log/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
													elif message[:5] == "USRL:":
														log("[INFO] ///User List/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
													else:
														log("[WARN] ///Bad parse - General error parsing data/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
											else:
												log("[WARN] Client (%s, %s) failed to complete sending a " + str(MessageLength) + " bit message within the timeout time of 6 seconds " % addr + " at : " + CurrentTime + "<br>")
								except Exception as e:
									log("[WARN] Error encountered at : " + CurrentTime + " : Due to exception in data processing code : " + str(e) + "<br>")
									continue
							else:
								log("[INFO] Client (%s, %s) has disconnected" % addr + " at : " + CurrentTime + "<br>")
								sock.close()
								CONNECTION_LIST.remove(sock)
								continue
						except Exception as e:
							log("[FATL] Error receiving data at : " + CurrentTime + "<br>")
							continue
			server_socket.close()
			log("[INFO] Attendance Server shutting down NOW, at : " + time.strftime("%Y/%m/%d-%H:%M:%S"))
	T1 = CheckCmdThread()
	T2 = CommManThread()
	# Start new Threads
	T1.start()
	T2.start()
