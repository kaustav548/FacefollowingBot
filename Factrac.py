import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2
import serial
import time

ser = serial.Serial('COM9', 9600)

def move_servos(angle1, angle2):
    command = f"{angle1},{angle2}\n"
    ser.write(command.encode())
    time.sleep(0.01) 

cap = cv2.VideoCapture(0)

detector = FaceDetector(minDetectionCon=0.5,modelSelection=0)

while True:
    
    success,img = cap.read()
    img,bboxs = detector.findFaces(img, draw=False)
    
    if bboxs :
        for bbox in bboxs :
            center = bbox["center"]
            x,y,w,h = bbox['bbox']
            score = int(bbox['score'][0]*100)
            lt_center = list(center)
            lt_center[0] = center[0]-310
            lt_center[1] = center[1]-226
            print(lt_center)
            t_center = tuple(lt_center)
            cv2.circle(img,center,5,(255,0,255),cv2.FILLED)
            cvzone.putTextRect(img,f'{score}%',(x,y - 10))
            cvzone.putTextRect(img,f'{t_center}',(50,50))
            cvzone.cornerRect(img,(x,y,w,h))
            angle1 = 90 - (lt_center[0]*60/300)
            angle2 = 90 - (lt_center[1]*60/200)
            move_servos(angle1, angle2)
            
    
    cv2.imshow("IMage",img)
    if cv2.waitKey(1)==13:
        cap.release()
        cv2.destroyAllWindows()
        break
    
    
    