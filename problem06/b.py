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
    for (x,y,w,h) in faces: 
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)  
        rec_gray = gray_img[y:y+h, x:x+w] 
        rec_color = image[y:y+h, x:x+w] 
    
        face = image[y:y+h,x:x+w]
    cv2.imshow("video", image)
    
    captured_emotions = emotion_detector.detect_emotions(image)
    print(captured_emotions)

    if cv2.waitKey(1) == 27: 
        break

cv2.destroyAllWindows()

# The Analyze() function will run analysis on every frame of the input video. 
# It will create a rectangular box around every image and show the emotion values next to that.
# Finally, the method will publish a new video that will have a box around the face of the human with live emotion values.
