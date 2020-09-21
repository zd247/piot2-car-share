import bluetooth
import keyboard
import cv2

#hciconfig hciX piscan


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Received [%s]" % data)
        if b'1' in data:
            exec(open("faceData.py").read())
        elif b'2' in data:
            exec(open("faceTraining.py").read())
        elif b'3' in data:
            exec(open("faceRecognition.py").read())
        elif b'4' in data:
            exec(open("barcodeScanner.py").read())

            
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")