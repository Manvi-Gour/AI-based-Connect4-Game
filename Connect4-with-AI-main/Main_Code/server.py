# TCP Server
# ==========
import socket
# Creatin a TCP/IP socket
serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Binding the socket to the port
serveraddress = ('localhost',12345)
print("Starting the server on %s port %s" % serveraddress)
serversock.bind(serveraddress)
# Listening to the incoming connections
serversock.listen(1)
while True:
# Waiting for a new connection
print("Waiting for a connection from a client ... ")
conn,clientaddress = serversock.accept()
try:
# Receiving the data fom the client and sending it again
print('Received Connection from',clientaddress)
while True:
data = conn.recv(1024)
print("Received data :", data.decode())
if data:
print("Sending data back to the client.")
conn.sendall(data)
else:
print("There is no more data.", clientaddress)
print("---------------")
break
finally:
# Closing the connection
conn.close()