#!/usr/bin/python
import cv2 as cv
import numpy as np
import os


def gstreamer_pipeline(
    sensor_id=0,
    sensor_mode=4,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            sensor_mode,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

if not os.path.isdir("img"):
    os.mkdir("img")

if not os.path.isdir("img/camera0"):
    os.mkdir("img/camera0")

if not os.path.isdir("img/camera1"):
    os.mkdir("img/camera1")

capture = cv.VideoCapture(gstreamer_pipeline(sensor_id=0),
                                                    cv.CAP_GSTREAMER)

if not capture.isOpened():
    print("Cannot open camera 0")
    exit()

capture_count = 20

while(capture_count):

    ret, image = capture.read()

    cv.imshow('frame', image)

    if cv.waitKey(1) & 0xFF == ord('c'):
        cv.imwrite("img/camera0/image"+str(capture_count)+".jpg", image)
        print("Captured "+"image"+str(capture_count)+".jpg")
        capture_count = capture_count - 1
        continue

capture.release()

capture = cv.VideoCapture(gstreamer_pipeline(sensor_id=1),
                                                    cv.CAP_GSTREAMER)

if not capture.isOpened():
    print("Cannot open camera 1")
    exit()

capture_count = 20

while(capture_count):

    ret, image = capture.read()

    cv.imshow('frame', image)

    if cv.waitKey(1) & 0xFF == ord('c'):
        cv.imwrite("img/camera1/image"+str(capture_count)+".jpg", image)
        print("Captured "+"image"+str(capture_count)+".jpg")
        capture_count = capture_count - 1
        continue

capture.release()
