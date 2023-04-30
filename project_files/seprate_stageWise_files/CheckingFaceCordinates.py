import cv2
import cvzone

from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

leftEye=[22,23,24,26,110,157,158,159,160,161,130,243]
# Up_lip_check=[50,62,63,64,54]
# down_lip_check=[49,61,68,67,66,65,55]
# all_points=[leftEye,Up_lip_check,down_lip_check]
while True:
    success,img=cap.read()

    img,faces=detector.findFaceMesh(img,draw=False)

    if faces:
        face=faces[0]
        # for id in range(73,85):  # 76,77,78,
        #     if id in [75,79,84]: #81,82,87,88,89
        #         continue
        for id in [80,82,87,88]:
            cv2.circle(img,face[id],5,(255,0,255),cv2.FILLED)

    cv2.imshow("Webcam",img)
    if cv2.waitKey(25) == ord('q'): # Press 'q' key to quit
        break


