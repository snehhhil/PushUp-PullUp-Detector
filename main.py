import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm



cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"


while cap.isOpened():
    ret, img = cap.read() #640 x 480
    #Determine dimensions of video - Help with creation of box in Line 43
    width  = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        left_elbow = detector.findAngle(img, 11, 13, 15)
        right_elbow = detector.findAngle(img, 12, 14, 16)
        left_shoulder = detector.findAngle(img, 13, 11, 23)
        right_shoulder = detector.findAngle(img, 14, 12, 24)
        left_hip = detector.findAngle(img, 11, 23, 25)
        right_hip = detector.findAngle(img, 12, 14, 26)
        left_wrist = detector.findAngle(img, 13, 15, 17)
        right_wrist = detector.findAngle(img, 14, 16, 18)
        
        #Percentage of success of pushup
        per = np.interp(left_elbow, (90, 160), (0, 100))
        
        #Bar to show Pushup progress
        bar = np.interp(left_elbow, (90, 160), (380, 50))

        #Check to ensure right form before starting the program
        if left_elbow > 160 and left_shoulder > 40 and left_hip > 160 and right_elbow > 160 and right_shoulder > 40 and right_hip > 160:
            form = 1
    
        #Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if left_elbow <= 90 and left_hip > 160 and right_elbow <= 90 and right_hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if left_elbow > 160 and left_shoulder > 40 and left_hip > 160 and right_elbow > 160 and right_shoulder > 40 and right_hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0

            #differentiating between a push up or a pull up            
            if left_wrist > 160 and right_wrist > 160:
                cv2.imshow("Pull Up Detected",img)
            elif left_wrist <= 90 and right_wrist <= 90:
                cv2.imshow ("Push Up Detected", img)
            else:
                cv2.imshow ("Neither a Push Up Nor a Pull UP", img)
        print(count)
        
        #Draw Bar
        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)


        #Pushup counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        
        #Feedback 
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

    cv2.imshow('Repetitions', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
       
