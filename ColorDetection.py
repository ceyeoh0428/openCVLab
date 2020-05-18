import cv2
import numpy as np


def empty(a):
    pass

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

path = 'src/butterfly.jpg'

# TrackBar
cv2.namedWindow('TrackBars')
cv2.resizeWindow('TrackBars', 400, 250)
cv2.createTrackbar('Hue Min', 'TrackBars', 0, 179, empty)  # opencv only provide 180
cv2.createTrackbar('Hue Max', 'TrackBars', 37, 179, empty)
cv2.createTrackbar('Sat Min', 'TrackBars', 118, 255, empty)
cv2.createTrackbar('Sat Max', 'TrackBars', 226, 255, empty)
cv2.createTrackbar('Val Min', 'TrackBars', 52, 255, empty)
cv2.createTrackbar('Val Max', 'TrackBars', 255, 255, empty)

while True:
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # black and white
    # threshold, imgBW = cv2.threshold(imgGray, 127, 255, cv2.THRESH_BINARY)

    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBars')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBars')
    s_min = cv2.getTrackbarPos('Sat Min', 'TrackBars')
    s_max = cv2.getTrackbarPos('Sat Max', 'TrackBars')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBars')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBars')
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResultUnmask = cv2.bitwise_and(img, img, mask=mask)
    imgResultMask = cv2.bitwise_and(img, imgHSV, mask=mask)

    overall = stackImages(0.4, ([imgGray, img, imgHSV], [mask, imgResultUnmask, imgResultMask]))
    cv2.imshow('Color Detection', overall)
    cv2.waitKey(1)
