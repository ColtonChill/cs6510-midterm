from fer import FER
import os
import sys
import pandas as pd
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# But the Face detection detector
emotion_detector = FER(mtcnn=True)
# Input the video for processing
#input_video = Video(location_videofile)

cam = cv2.VideoCapture(0)
result, image = cam.read()
while True:
    # Capture all the emotions on the image

    success, image = cam.read()
    image = cv2.flip(image, 1)
    if not success:
        print("!!! Failed vid.read()")
        break

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray_img, 1.25, 4)
    for i in range(len(faces)): 
        (x,y,w,h) = faces[i]
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)  
        rec_gray = gray_img[y:y+h, x:x+w] 
        rec_color = image[y:y+h, x:x+w] 

        captured_emotions = emotion_detector.detect_emotions(image)
        if len(captured_emotions) == len(faces):
            emotions = captured_emotions[i]['emotions']
            offset = 20
            for key in emotions.keys():
                cv2.putText(img=image, text=(str(key) + ": " + str(emotions[key])), org=(x, y+h+offset), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.5, color=(0, 255, 0),thickness=1)
                offset += 20
    cv2.imshow("video", image)

    if cv2.waitKey(1) == 27: 
        break

cv2.destroyAllWindows()
