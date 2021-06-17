#!/usr/bin/python
import numpy as np
import cv2 as cv
import os


capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Cannot open camera")
    exit()

capture_count = 10

if not os.path.isdir("img"):
    os.mkdir("img")

while(capture_count):

    ret, image = capture.read()

    cv.imshow('frame', image)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('c'):
        cv.imwrite("img/image"+str(capture_count)+".jpg", image)
        print("Captured "+"image"+str(capture_count)+".jpg")
        capture_count = capture_count - 1
        continue

capture.release()
