import cv2
import numpy as np


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


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for shapes in contours:
        area = cv2.contourArea(shapes)
        if area > 500:
            print(area)
            cv2.drawContours(imgContour, shapes, -1, (0, 0, 255), 3)
            perimeter = cv2.arcLength(shapes, True)
            print(perimeter)
            approxCorner = cv2.approxPolyDP(shapes, 0.02 * perimeter, True)
            objCorner = len(approxCorner)
            print(objCorner)
            x, y, w, h = cv2.boundingRect(approxCorner)

            if objCorner == 3:
                obj = 'Triangle'
            elif objCorner == 4:
                ratio = w / float(h)
                if ratio > 0.95 and ratio < 1.05:
                    obj = 'Square'
                else:
                    obj = 'Rectangle'
            elif objCorner > 4:
                obj = 'Circle'
            else:
                obj = 'None'

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imgContour, obj, ((x + (w // 2) - 25, y + (h // 2) + 10)), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 0, 255), 1)


path = 'src/shapes.png'
img = cv2.imread(path)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 2)
imgCanny = cv2.Canny(imgBlur, 30, 30)
imgContour = img.copy()
imgBlank = np.zeros_like(img)

getContours(imgCanny)

overview = stackImages(0.6, ([imgBlank, img], [imgGray, imgBlur], [imgCanny, imgContour]))
cv2.imshow('shapes', overview)
cv2.waitKey(0)
