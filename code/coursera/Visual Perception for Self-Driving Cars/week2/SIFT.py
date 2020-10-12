import numpy as np
from cv2 import cv2

img = cv2.imread("street.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 需安装包opencv_contrib_python
sift = cv2.xfeatures2d.SIFT_create()
kp = sift.detect(gray, None)
img = cv2.drawKeypoints(gray, kp, img)

# cv2.imwrite('sift_keypoints.jpg',img)
img = cv2.drawKeypoints(gray, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imwrite("sift_keypoints.jpg", img)

