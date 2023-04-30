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