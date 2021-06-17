#!/usr/bin/python
import numpy as np
import cv2 as cv

capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Cannot open camera")
    exit()

cal_file = cv.FileStorage("cal_data.xml", cv.FileStorage_READ)

mtx = cal_file.getNode("CameraMatrix").mat()
dist = cal_file.getNode("Distortion").mat()
cal_file.release()

while (True):
    ret, img = capture.read()
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR , borderMode=cv.BORDER_CONSTANT)
    cv.imshow('img', dst)
    cv.waitKey(1)
