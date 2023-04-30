import cv2
import cvzone
import pyautogui
import time

import mediapipe
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plot_y=LivePlot(640,360,[20,50],invert=True)

leftEye=[22,23,24,26,110,157,158,159,160,161,130,243]
upper_lip=[82] #80
lower_lip=[87] #88

ratio_list=[]
left_mouse_click=""
right_mouse_click=""
counter = 0
left_color=(255,0,255)
right_color=(255,0,255)
screen_w, screen_h = pyautogui.size()


while True:
    success,img=cap.read()
    img = cv2.flip(img, 1)

    img,faces=detector.findFaceMesh(img,draw=False)

    if faces:
        face=faces[0]

        # Left Eye

        for position in [leftEye,upper_lip,lower_lip]:
            for id in position:
                cv2.circle(img,face[id],5,(255,0,255),cv2.FILLED)

        left_up=face[159]
        left_down=face[23]
        left_left=face[130]
        left_right=face[243]

        # Ratio of frame and screen should be equal ??
        """ 
        (x/frame_x)need something to multiply ??  = mouse_x/screen_x
        mouse_x=((x/frame_x)*(?))*screen_x
        """

        frm_x,frm_y,frm_z=img.shape
        mouse_x=(left_up[0]/frm_x)*screen_w
        mouse_y=(left_up[1]/frm_y)*screen_h


        # print(mouse_x,mouse_y)
        try: 
            pyautogui.moveTo(mouse_x,mouse_y)
        except:
            pass
        lip_up=face[80]
        lip_down=face[87]

        mouth_dist, *unwanted = detector.findDistance(lip_up,lip_down)
        # print(mouth_dist)  # open >> 27+      close >> 16-

        len_ver , *unwanted = detector.findDistance(left_up,left_down)
        len_hor , *unwanted = detector.findDistance(left_left,left_right)

        cv2.line(img,left_up,left_down,(0,200,0),3)
        cv2.line(img,left_left,left_right,(0,200,0),3)

        ratio = (len_ver/len_hor)*100

        ratio_list.append(ratio)

        if len(ratio_list)>10:
            ratio_list.pop(0)

        ratio_avg = sum(ratio_list)/len(ratio_list)

        # to click person has to open mouth and then he has to widden eye for left click and shorten eye for right click
        if mouth_dist >27: 
            if ratio_avg<24 and counter==0:
                pyautogui.click(button='right')
                right_mouse_click="Clicked"
                time.sleep(1)
                counter = 1
                right_color = (0,200,0)

            elif ratio_avg>40 and counter==0:
                pyautogui.click()
                left_mouse_click="Clicked"
                time.sleep(1)
                counter = 1
                left_color = (0,200,0)

            if counter!=0:
                counter+=1
                if counter>10:
                    counter = 0
                    left_color=(255,0,255)
                    right_color=(255,0,255)
        # need to connect eye movement with mouse (mouth shut)
        else:
            left_mouse_click=right_mouse_click=""
            pass

        cvzone.putTextRect(img,f'left:', (25,100))
        cvzone.putTextRect(img,f'{left_mouse_click}', (25,150),colorR=left_color)
        cvzone.putTextRect(img,f'right:', (450,100))
        cvzone.putTextRect(img,f'{right_mouse_click}', (450,150),colorR=right_color)

        img_Plot =plot_y.update(ratio_avg)
        img = cv2.resize(img,(640,360)) 
        image_Stack=cvzone.stackImages([img,img_Plot],2,1)
    
    else:
        # need to write condition if no face detect
        image_Stack=cvzone.stackImages([img,img],2,1)
        pass

    img = cv2.resize(img,(640,360)) 
    cv2.imshow("Webcam",image_Stack)
    if cv2.waitKey(25) == ord('q'): # q >> quit
        break
