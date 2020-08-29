import socket
import jwt

key='secret'

HOST = '' # Server IP or Hostname
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#managing error exception
try:
	s.bind((HOST, PORT))
	except socket.error:
	print 'Bind failed '

	s.listen(5)
	print 'Socket awaiting messages'
	(conn, addr) = s.accept()
	print 'Connected'

# awaiting for message
while True:
	data = conn.recv(1024)
	decoded = jwt.decode(data, key, algorithms='HS256')
	print 'I sent a message back in response to: ' + decoded
	reply = ''

	# process your message
	if 'Auth' in decoded:
		reply = 'Authenticating ...!'
		#check if authentication is correct and reply

	#and so on and on until...
	elif decoded == 'quit':
		conn.send('Terminating')
		break
	else:
		reply = 'Unknown command'

	# Sending reply
	reply = jwt.encode(reply, key, algorithm='HS256')
	conn.send(reply)
	conn.close() # Close connections
