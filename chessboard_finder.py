#!/usr/bin/python
import numpy as np
import cv2 as cv
import os


capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Cannot open camera")
    exit()

while(True):

    ret, image = capture.read()

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, (10,6), flags=cv.CALIB_CB_ADAPTIVE_THRESH+cv.CALIB_CB_NORMALIZE_IMAGE)
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("faund")
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(image, (10,6), corners2, ret)

    cv.imshow('img', image)
    cv.waitKey(1)

capture.release()
