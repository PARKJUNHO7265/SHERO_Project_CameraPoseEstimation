'''
Programming Lab : AVSC , SungKyunKwan University
                  (Autonomous Vehicle Separating and Coupling)
     Written by
             JunHo Park, JinSeok Park, HyunWoong Jeong, JuHeon Lee, YoungYook Hong, JinWoo Lim
             School of Electrical and Electronics Engineering (PARK)
             School of Software Programming (Jeong)
             School of Mechanical Engineering Department (Lee, Hong, Lim)
             Sungkyunkwan University.
 
     Advisor : JaeWook Jeon
             Professor of
             School of Electrical and Electronics Engineering
             Sungkyunkwan University.
 
     Leader  : YoongHyun Kwon
             School of Electrical, Electronics and Computer Engineering
             Sungkyunkwan University.
     
     Mentor  : SungCheon Park
             Electronics and Telecommunications Research Institute
             
     File name : NewPoseEst.py
     
     Written on Oct 30, 2020
'''

import numpy as np

import cv2

import math

import time

import webbrowser

import os



# Function of Drawing the x axis blue, y axis green, z axis red

def draw(img, corners, imgpts):

    corner = tuple(corners[0].ravel())

    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)

    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)

    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)

    return img

# Function of Pose estimation of Camera

def poseEstimation():

    prev_time = 0

    FPS = 1

    #Bring the value of .npz file

    with np.load('calib.npz') as X:

        ret, mtx, dist, _, _ = [X[i] for i in ('ret', 'mtx', 'dist', 'rvecs', 'tvecs')]

    # Iteration and Accuracy for find 6x7 chess board

    termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((6*7,3),np.float32)

    objp[:,:2] = np.mgrid[0:6, 0:7].T.reshape(-1,2)

    axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

    objpoints=[]

    imgpoints=[]

    cap=cv2.VideoCapture(1)

    # Frame size 1920x1080

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)

    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

    while True:

        ret, frame = cap.read()

        current_time = time.time() - prev_time

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray,(6,7),None)

        if (ret == True) and (current_time>1./FPS):  #For control frame of camera

            prev_time = time.time()

            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1), termination)

            #Find the rvecs tvecs of chess board in video

            _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)

            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

            #Draw the axis

            frame = draw(frame, corners, imgpts)

            cv2.imshow('frame',frame)

            # Send Signal to arduino for control motor movement

            if ((rvecs[0]<-0.18) or (rvecs[1]>0.18)) and (tvecs[2]>80):       

               webbrowser.open('192.168.4.1/M1',new=1)
               time.sleep(1)
               os.system("taskkill /im iexplore.exe /f")
               print("M1")
               

            elif((rvecs[0]>0.18) or (rvecs[1]<-0.18)) and (tvecs[2]>80):

                webbrowser.open('192.168.4.1/M2',new=1)
                time.sleep(1)
                os.system("taskkill /im iexplore.exe /f")
                print("M2")

                
                
            elif(rvecs[0]<0.18) and (rvecs[0]>-0.18) and (rvecs[1]<0.18) and (rvecs[1]>-0.18) and (tvecs[2]>80):

                webbrowser.open('192.168.4.1/M3',new=1)
                time.sleep(1)
                os.system("taskkill /im iexplore.exe /f")
                print("M3")

            
                
            # Minimum distance to recognize chessboard with camera
            
            elif(tvecs[2]<80):
                print("Minimum distance")
                webbrowser.open('192.168.4.1/M4',new=1)
                time.sleep(1)
                os.system("taskkill /im iexplore.exe /f")
                print("M4")
                
            

            #Value of rvecs and tvecs

            print(rvecs[0])

            print(rvecs[1])

            print(tvecs[2])

            print('\n')

            

        k = cv2.waitKey(1) & 0xFF

        if k==27:

            break

    cap.release()

    cv2.destroyAllWindows()

 
poseEstimation()
