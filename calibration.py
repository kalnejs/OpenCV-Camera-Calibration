#!/usr/bin/python
import numpy as np
import cv2 as cv
import os
import glob


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


images = glob.glob('img/*.jpg')

for fname in images:
    img = cv.imread(fname)
    cv.imshow("mask image", img)
    print(fname)

    # blur_img = cv.GaussianBlur(img, (0, 0), 5)
    # usm = cv.addWeighted(img, 1.5, blur_img, -0.5, 0)
    # gray = cv.cvtColor(usm, cv.COLOR_BGR2GRAY)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow("mask image", gray)
    cv.waitKey(0)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (10,6))
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("faund")
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (11,6), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(0)

cv.destroyAllWindows()
