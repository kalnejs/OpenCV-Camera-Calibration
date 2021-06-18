#!/usr/bin/python
import numpy as np
import cv2 as cv

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

capture_camera0 = cv.VideoCapture(gstreamer_pipeline(sensor_id=0),
                                                    cv.CAP_GSTREAMER)
if not capture_camera0.isOpened():
    print("Cannot open camera 0")
    exit()

capture_camera1 = cv.VideoCapture(gstreamer_pipeline(sensor_id=1),
                                                    cv.CAP_GSTREAMER)
if not capture_camera1.isOpened():
    print("Cannot open camera 1")
    exit()

cal_file_camera0 = cv.FileStorage("cal_data_camera0.xml", cv.FileStorage_READ)

mtx_camera0 = cal_file_camera0.getNode("CameraMatrix").mat()
dist_camera0 = cal_file_camera0.getNode("Distortion").mat()
cal_file_camera0.release()

cal_file_camera1 = cv.FileStorage("cal_data_camera1.xml", cv.FileStorage_READ)

mtx_camera1 = cal_file_camera1.getNode("CameraMatrix").mat()
dist_camera1 = cal_file_camera1.getNode("Distortion").mat()
cal_file_camera1.release()

while (True):

    ret0, img0 = capture_camera0.read()
    h0,  w0 = img0.shape[:2]
    newcameramtx0, roi0 = cv.getOptimalNewCameraMatrix(mtx0, dist0, (w0,h0), 1, (w0,h0))
    mapx0, mapy0 = cv.initUndistortRectifyMap(mtx0, dist0, None, newcameramtx0, (w0,h0), 5)
    dst0 = cv.remap(img0, mapx0, mapy0, cv.INTER_LINEAR , borderMode=cv.BORDER_CONSTANT)
    cv.imshow('img', dst0)

    ret1, img1 = capture_camera1.read()
    h1,  w1 = img1.shape[:2]
    newcameramtx1, roi1 = cv.getOptimalNewCameraMatrix(mtx1, dist1, (w1,h1), 1, (w1,h1))
    mapx1, mapy1 = cv.initUndistortRectifyMap(mtx1, dist1, None, newcameramtx1, (w1,h1), 5)
    dst1 = cv.remap(img1, mapx1, mapy1, cv.INTER_LINEAR , borderMode=cv.BORDER_CONSTANT)
    cv.imshow('img', dst1)

    cv.waitKey(1)
