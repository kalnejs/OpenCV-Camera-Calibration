#!/usr/bin/python
import numpy as np
import cv2 as cv
import os

chessboard_cols = 9
chessboard_rows = 6

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboard_cols*chessboard_rows,3), np.float32)
objp[:,:2] = np.mgrid[0:chessboard_cols,0:chessboard_rows].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Cannot open camera")
    exit()

cals_saved = 0
max_saves = 40
while(max_saves):

    ret, img = capture.read()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (chessboard_cols,chessboard_rows), None)
    # If found, add object points, image points (after refining them)
    if ret == True and (cv.waitKey(10) & 0xFF == ord('q')):
        cals_saved = cals_saved + 1
        max_saves = max_saves - 1
        print(cals_saved)
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (chessboard_cols,chessboard_rows), corners2, ret)
    cv.imshow('img', img)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

ret, img = capture.read()
cv.imshow('img', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

while (True):
    ret, img = capture.read()
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR , borderMode=cv.BORDER_CONSTANT)
    cv.imshow('img', dst)
    cv.waitKey(1)
