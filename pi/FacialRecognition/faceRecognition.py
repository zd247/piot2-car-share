''''
Real Time Face Recogition
    ==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
    ==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
start = time.time()
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
i = 100
id = 0
list = os.listdir("/home/pi/Downloads/piot2-car-share/pi/FacialRecognition/dataset")
number_of_files = len(list)
face_id = str((number_of_files/30)+1)
# names related to ids: example ==> Marcelo: id=1,  etc
names = ["None"]
for i in range(len(face_id)):
    u = i+1
    names.append("User " +str(u))


# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    now = time.time()
    ret, img =cam.read()
    img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            i = confidence
            id = names[id]
            confident = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            i = 100
            confident = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confident), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img)
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    if ((id != 'unknown') and (str(id) != '0') and (int(100-i) < 20) and (round(int(now-start),0)>5)):
        print("Car door opened for id:" + str(id) + " w conf: " + str(round(i, 2)))
        break

# Do a bit of cleanup
cam.release()
cv2.destroyAllWindows()
