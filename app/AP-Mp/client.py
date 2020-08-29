import socket
import jwt


key = 'secret'

HOST = '' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
	command = raw_input('Enter your message to encrypt:')
	encoded = jwt.encode(command, key, algorithm='HS256')
	s.send(encoded)
	reply = s.recv(1024)
	reply = jwt.decode(replt, key, algorithms='HS256')
		if reply == 'Terminate':
			break
		print reply
