#!/usr/bin/python
import numpy as np
import cv2 as cv
import os
import glob

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


images_camera0 = glob.glob('img/camera0/*.jpg')

for fname in images_camera0:
    img = cv.imread(fname)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (chessboard_cols,chessboard_rows), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (chessboard_cols,chessboard_rows), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(200)

cv.destroyAllWindows()

img = cv.imread(images_camera0[0])
cv.imshow('img', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

cal_file = cv.FileStorage("cal_data_camera0.xml", cv.FileStorage_WRITE)
cal_file.write("CameraMatrix", mtx)
cal_file.write("Distortion", dist)
cal_file.release()





# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboard_cols*chessboard_rows,3), np.float32)
objp[:,:2] = np.mgrid[0:chessboard_cols,0:chessboard_rows].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


images_camera1 = glob.glob('img/camera1/*.jpg')

for fname in images_camera1:
    img = cv.imread(fname)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (chessboard_cols,chessboard_rows), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (chessboard_cols,chessboard_rows), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(200)

cv.destroyAllWindows()

img = cv.imread(images_camera1[0])
cv.imshow('img', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

cal_file = cv.FileStorage("cal_data_camera1.xml", cv.FileStorage_WRITE)
cal_file.write("CameraMatrix", mtx)
cal_file.write("Distortion", dist)
cal_file.release()
