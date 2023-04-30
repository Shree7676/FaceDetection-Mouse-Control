import cv2
import cvzone

from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plot_y=LivePlot(640,360,[20,50],invert=True)

leftEye=[22,23,24,26,110,157,158,159,160,161,130,243]
ratio_list=[]
left_mouse_click=0
right_mouse_click=0
counter = 0
color=(255,0,255)

while True:
    success,img=cap.read()

    img,faces=detector.findFaceMesh(img,draw=False)

    if faces:
        face=faces[0]
        for id in leftEye:
            cv2.circle(img,face[id],5,color,cv2.FILLED)

        left_up=face[159]
        left_down=face[23]
        left_left=face[130]
        left_right=face[243]

        len_ver , *unwanted = detector.findDistance(left_up,left_down)
        len_hor , *unwanted = detector.findDistance(left_left,left_right)

        cv2.line(img,left_up,left_down,(0,200,0),3)
        cv2.line(img,left_left,left_right,(0,200,0),3)

        ratio = (len_ver/len_hor)*100

        ratio_list.append(ratio)

        if len(ratio_list)>10:
            ratio_list.pop(0)

        ratio_avg = sum(ratio_list)/len(ratio_list)

        if ratio_avg<30 and counter==0:
            left_mouse_click+=1
            counter = 1
            color = (0,200,0)
        if ratio_avg>40 and counter==0:
            right_mouse_click+=1
            counter = 1
            color = (0,200,0)
        if counter!=0:
            counter+=1
            if counter>10:
                counter = 0
                color=(255,0,255)

        cvzone.putTextRect(img,f'left click: {left_mouse_click}', (50,100),colorR=color)
        cvzone.putTextRect(img,f'right click: {right_mouse_click}', (50,300),colorR=color)

        img_Plot =plot_y.update(ratio_avg)
        img = cv2.resize(img,(640,360)) 
        image_Stack=cvzone.stackImages([img,img_Plot],2,1)
    
    else:
        # need to write condition if no face detect
        image_Stack=cvzone.stackImages([img,img],2,1)
        pass

    img = cv2.resize(img,(640,360)) 
    cv2.imshow("Webcam",image_Stack)
    if cv2.waitKey(25) == ord('q'): # Press 'q' key to quit
        break