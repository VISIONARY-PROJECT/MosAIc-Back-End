import numpy as np
import cv2
import uuid

def detect_face(img):
    image = cv2.imread(img)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(image, 1.2)
    if len(faces):
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        id = str(uuid.uuid4())[:12]
        cv2.imwrite("static/img/{}.jpeg".format(id),image)
        return id
    else:
        return None