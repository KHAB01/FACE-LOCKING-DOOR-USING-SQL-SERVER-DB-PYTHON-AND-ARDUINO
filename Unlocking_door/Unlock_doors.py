import os
import cv2
import face_recognition
import numpy as np
import pyodbc
import pyttsx3 as textSpeach
import serial
import time


x=0
m=0
d=0

def arduinno_conn(x, d, m):
    if x >= 5:
        m = 1
        ard = serial.Serial('com3', 9600)
        time.sleep(2)
        var = 'a'
        c = var.encode()
        textSpeach.speak(
            "Face recognition complete..it is matching with database...welcome..sir..Door is openning for 5 seconds")
        ard.write(c)
        time.sleep(4)
    elif d == 10:
        textSpeach.speak("face is not found please try again ")
    if m == 1:
        textSpeach.speak("door is closing")


video_capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

connection_string = pyodbc.connect('Driver={SQL Server};'
                      'Server=KHAOULA\SQLEXPRESS;'
                      'Database=face_recognition;'
                      'Trusted_Connection=yes;')

mycursor = connection_string.cursor()
mycursor.execute("select * from ImageDB")
engine = textSpeach.init()
rows = mycursor.fetchall()

known_face_names=[]
known_face_encodings =[]

for r in rows:
    db_enc = np.frombuffer(r[1])
    known_face_encodings.append(db_enc)
    known_face_names.append(r[0])


while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
        name = "unknown"
        d+=1

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            x+=1

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 16, bottom - 16), font, 1.0, (255, 255, 255), 1)
        arduinno_conn(x,d,m)

    cv2.imshow('Video', frame)
    k = cv2.waitKey(1) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

video_capture.release()
cv2.destroyAllWindows()