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
	if 'MAC:' in decoded:
 		with open('/home/pi/iot/piot2-car-share/app/AP-Mp/mp/macaddress.csv', 'a', newline ='') as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for macaddress in csv_reader:
				for i in macaddress:
					if macaddress[i].strip() == decoded.strip():
						reply = 'Authenticated'
					else:
						reply = 'Access denied'


	# Sending reply
	reply = jwt.encode(reply, key, algorithm='HS256')
	conn.send(reply)
	conn.close() # Close connections
