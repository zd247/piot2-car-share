import socket
import jwt
from bluetooth import bluetooth
import os
import time

key = 'secret'

HOST = '10.247.230.60' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

target_name = input("enter your device name to verify")
target_address = None

def lookUpNearbyBluetoothDevices():
 nearby_devices = bluetooth.discover_devices()
 for bdaddr in nearby_devices:
  if target_name == bluetooth.lookup_name( bdaddr ):
   print(bdaddr)
   global target_address
   target_address = bdaddr
   break
 if target_address is not None:
  print ("found target bluetooth device with address ", target_address)
 else:
  print ("could not find target bluetooth device nearby")

def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)

  client_sock,address = server_sock.accept()
  print("Accepted connection from " + str(address))

  data = client_sock.recv(1024)
  print("received [%s]" % data)

  client_sock.close()
  server_sock.close()

def sendMessageTo(message):
 port = 8
 sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
 if target_address is not None:
  sock.connect((target_address, port))
  sock.send(message)
  print("Sent")
 else:
  print("No device connected")
 sock.close()

#Lets loop awaiting for your input
while True:
    lookUpNearbyBluetoothDevices()

    encoded = jwt.encode(target_name, key, algorithm='HS256')
    s.send(encoded)
    reply = s.recv(1024)
    reply = jwt.decode(reply, key, algorithms='HS256')
    sendMessageTo(reply)
    print('Sent' + reply)
