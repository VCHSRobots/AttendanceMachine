# -*- coding: utf-8 -*-
# Compiled with Python version 2.7.9
import socket, time, select, threading
text = """<!---------- CSS ----------->

<style>
        body
        {
                background-color: black;
        }
        h1
        {
                font-family: monospace;
                text-align: center;
                color: red;
                text-shadow: 50px 50px 5px #f00000;
        }
        p1
        {
                font-family: monospace;
                color: gray;
        }
        p2
        {
                font-family: monospace;
                color: white;
        }
        p3
        {
                font-family: monospace;
                color: green;
        }
</style>

<!----------- HTML -------------->

<head>
    <title>Scanner Logs</title>
    <meta http-equiv="refresh" content="2" />
</head>
<body>
<h1>
/-----------------------\<br>
| LIVE SCANNER LOG FEED |<br>
\-----------------------/<br>
</h1>
<p1>
This page should refresh every /2/ seconds with live log data.<br>
To reduce clutter, log data will be removed from here every /8/ minutes.<br>
<br>
If you would like to use any of the "special" commands, grab a socket testing software of your choice (I recommend using "https://sourceforge.net/projects/sockettest/"), and send your message to:<br>
[Address: "epicarg.xyz" Port: "3265"]<br>
Only /3/ clients may connect properly at one time. That number is arbatrary.<br>
<br>
/!\ Please note that these commands (and this entire page!) are just a temporary feature, because I don't really know how to interact with this server's communications manager script from a html webpage...<br>
In any case, your message will be sent to the comm script, which will then send them to the scanner as a reply. In the future, this will be handeled differently; the comm script will be given messages to send to the scanner directly from the client clicking buttons on the html page. (Or something along those lines.)<br>
<br>
Also, not all of these commands, at the time of this writing, are functional. I'll mark functional commands with a "*" prefix as I update the scanner's software and push it to GitHub.<br>
Here is the list of special commands which you can send to test out requesting (and sending) special data to the scanner:<br>
Please note the addition of the headers to each of these commands. This is so we don't have to add in a special instance for each "command".<br>
</p1>
<br>
<p2>
* <4>rqln - Request a copy of the newest log<br>
* <4>rqla - Request copies of all avaliable logs<br>
* <4>rqul - Request a copy of the scanner's userlist<br>
X <4>psul - Send the scanner a copy of the webserver's userlist<br>
* <4>tgdm - Toggle the scanner's demo video<br>
</p2>
<br>
<p3>
-------------------------------------------------------------------<br>
LOG STARTS HERE:<br>
-------------------------------------------------------------------<br>
"""
def ClearPage():
    threading.Timer(480, ClearPage).start()
    with open("index.html", "w") as file:
        file.write(text)
ClearPage()
####################
# Main Server Code #
####################
if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 8192
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
            if socket != server_socket and socket != sock:
                try:
                    socket.send(message)
                    log("[INFO] ///Broadcast/// message: " + message + ": Sent to client (%s, %s)" %addr + " at " + CurrentTime + "<br>")
                except:
                    log("[WARN] Failed to send ///Broadcast/// message to client (%s, %s)" %addr + ": Removing from client list")
                    socket.close()
                    CONNECTION_LIST.remove(socket)
    def log(msg):
        print(msg)
        with open("index.html", "a") as file:
            file.write(msg)
    log("[INFO] Attendance Server initiated on port " + str(PORT) + " at : " + time.strftime("%Y/%m/%d-%H:%M:%S") + "<br>")
    message = ""
    EOH = False
    timeout = False
    def DataTimeout():
        threading.Timer(6, DataTimeout).start()
        timeout = True
    DataTimeout()
    while True: 
        CurrentTime = time.strftime("%Y/%m/%d-%H:%M:%S")
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                log("[INFO] Client (%s, %s) has connected" % addr + " at : " + CurrentTime  + "<br>")
            else:
                RecvLength = 0
                MessageLength = 0
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data != "":
                        DataTimeout()
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
                                        RecvLength = 0 - hlength
                                        MessageLength = int(mlength)
                                        EOH = True
                            else:
                                log("[WARN] ///Bad parse - No Start-Of-Header symbol/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + data + "<br>")
                        message += data
                        RecvLength += len(data)
                        if timeout == False:
                            if RecvLength >= MessageLength:
                                message = message.split('>', 1)[-1]
                                if message[:5] == "SCAN:":
                                    log("[INFO] ///Scan/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "!")
                                elif message[:5] == "LOGN:":
                                    log("[INFO] ///Newest Log/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "!")
                                elif message[:5] == "LOGA:":
                                    log("[INFO] ///All Logs/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "!")
                                elif message[:5] == "USRL:":
                                    log("[INFO] ///User List/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "!")
                                #Following are the temporary commands used to communicate with clients. These will be replaced in the actual release of the client/server for the Attendance system.
                                elif message[:4] == "rqln":
                                    #Send request to client(s) for newest log
                                    log("[INFO] ///Pull Newest Log from Scanner to Server/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "rqln")
                                elif message[:4] == "rqla":
                                    #Send request to client(s) for all logs
                                    log("[INFO] ///Pull All Logs from Scanner to Server/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "rqla")
                                elif message[:4] == "rqul":
                                    #Send request to client(s) for UserList
                                    log("[INFO] ///Pull UserList from Scanner to Server/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "rqul")
                                elif message[:4] == "psul":
                                    log("[INFO] ///Push UserList from Server to Scanner/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "psul")
                                elif message[:4] == "tgdm":
                                    #Send request to client(s) to toggle the demo video.
                                    log("[INFO] ///Toggle Demo/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                    broadcast_data(sock, "tgdm")
                                else:
                                    log("[WARN] ///Bad parse - General error parsing data/// message recieved from client (%s, %s) at : " % addr + CurrentTime + " : " + message + "<br>")
                                RecvLength = 0
                                MessageLength = 0
                                EOH = False
                        else:
                            log("[WARN] Client (%s, %s) failed to complete sending a " + str(MessageLength) + " bit message within the timeout time of 6 seconds " % addr + " at : " + CurrentTime + "<br>") 
                    else:
                        log("[INFO] Client (%s, %s) has disconnected" % addr + " at : " + CurrentTime + "<br>")
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                        continue
                except Exception as e:
                    log("[WARN] Client (%s, %s) has disconnected" % addr + " at : " + CurrentTime + " : Due to exception in data processing code : " + str(e) + "<br>")
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
