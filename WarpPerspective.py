import cv2
import numpy as np

path = 'src/cards.jpg'
img = cv2.imread(path)
width, height = 250, 350
p1 = np.float32([[301, 69], [457, 71], [308, 260], [484, 251]])
p2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(p1, p2)
output = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow('Original', img)
cv2.imshow('Output', output)
cv2.waitKey(0)
