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

 
# Function of Camera Calibration

def saveCamCalibration():

    # Criteria of chess board

    termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 100)

    objp = np.zeros((6*7,3),np.float32)

    objp[:,:2] = np.mgrid[0:6, 0:7].T.reshape(-1,2)

    objpoints=[]

    imgpoints=[]

    # Video start

    cap = cv2.VideoCapture(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)

    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

    count = 0

    while True:

        #Make video to frames

        fet, frame = cap.read()

        #Make color of frames to gray

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Find corner of chess board

        ret, corners = cv2.findChessboardCorners(gray,(6,7),None)

        # If find corners of chess board

        if ret:

            objpoints.append(objp)

            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1), termination)

            imgpoints.append(corners)

            cv2.drawChessboardCorners(frame,(6,7),corners,ret)

            count += 1

            print('[%d]'%count)

        #Show image of chess board corners

        cv2.imshow('img',frame)

        #Wait until esc

        k=cv2.waitKey(0)

        if k==27:

            break

        if count > 5:

            break

    cap.release()

    cv2.destroyAllWindows()

    #Get the value of calibration

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,

                                                 gray.shape[::-1],None,None)

    #Save the value to .npz file

    np.savez('calib.npz',ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    count = 0

    print('It has been stored\n')

 

saveCamCalibration()
