import socket
# Creatin a TCP/IP socket
serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def sendmsg():
 # print("Enter your msg : ")
 msg = input("Enter your msg : ")
 return msg
# Binding the socket to the port
serveraddress = ('localhost',8000)
print("Starting the server on %s port %s" % serveraddress)
serversock.bind(serveraddress)
# Listening to the incoming connections
serversock.listen(1)
while True:
# Waiting for a new connection
print("Waiting for a connection from a client ... ")
conn,clientaddress = serversock.accept()
try:
 print('Received Connection from',clientaddress)
 while True:
 data = conn.recv(1024)
 print("Received data :", data.decode())
 if data:
     data = sendmsg()
 print("Sending data back to the client.")
 conn.sendall(data.encode('utf-8'))
 else:
 print("There is no more data.", clientaddress)
 print("---------------")
 break
finally:
    conn.close(