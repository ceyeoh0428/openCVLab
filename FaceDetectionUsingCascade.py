import cv2

facesCascade = cv2.CascadeClassifier('src/haarcascade_frontalface_default.xml')
img = cv2.imread('src/people.png')
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = facesCascade.detectMultiScale(imgGray, 1.1, 4)
for x, y, w, h in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
cv2.imshow('people', img)
cv2.waitKey(0)
