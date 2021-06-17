#!/usr/bin/python
import numpy as np
import cv2 as cv
import os
import glob

chessboard_cols = 9
chessboard_rows = 6

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 1e-3)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((1, chessboard_cols*chessboard_rows, 3), np.float32)
objp[0,:,:2] = np.mgrid[0:chessboard_cols,0:chessboard_rows].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


images = glob.glob('img/*.jpg')

for fname in images:
    img = cv.imread(fname)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (chessboard_cols,chessboard_rows), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (3,3), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (chessboard_cols,chessboard_rows), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(0)

cv.destroyAllWindows()

img = cv.imread(images[0])
cv.imshow('img', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, K, D, rvecs, tvecs = cv.fisheye.calibrate(objpoints, imgpoints, gray.shape[::-1], None, None)

print(K)
cv.waitKey(0)
print(D)

capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Cannot open camera")
    exit()

while (True):
    ret, img = capture.read()
    h,  w = img.shape[:2]
    mapx, mapy = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, (w,h), cv.CV_16SC2)
    dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    cv.imshow('img', dst)
    cv.waitKey(1)
