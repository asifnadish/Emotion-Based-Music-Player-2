import cv2
from deepface import DeepFace
import numpy

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



class DetectEmotion(object):
    def __init__(self):
        self.cap=cv2.VideoCapture(1)
        if not self.cap.isOpened():
            self.cap=cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot Open The Webcam")
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        ret,frame=self.cap.read()

        result= DeepFace.analyze(frame, actions=["emotion"])

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces= faceCascade.detectMultiScale(gray,1.1,4)
    
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            
        font= cv2.FONT_HERSHEY_SIMPLEX   
        cv2.putText(frame, 
              result['dominant_emotion'],
              (50,50),
              font, 3,
              (0,0,255),
              2,
              cv2.LINE_4)
        #cv2.imshow('Original video', frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(),result['dominant_emotion'])
