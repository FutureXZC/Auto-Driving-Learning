import numpy as np
from cv2 import cv2

filename = 'chessboard.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
# @param:
# InputArray image: 输入图像
# InputOutputArray corners: 角点（既作为输入也作为输出）
# Size winSize: 计算亚像素角点时考虑的区域的大小，大小为N * N; N = (winSize * 2 + 1)
# Size zeroZone: 类似于winSize，但是总是具有较小的范围，通常忽略（即Size(-1, -1)）
# TermCriteria criteria: 表示计算亚像素时停止迭代的标准，可选的值有Term_Criteria_MAX_ITER 、
#                        Term_Criteria_EPS（可以是两者其一，或两者均选），前者表示迭代次数达到了最大次数时停止，
#                        后者表示角点位置变化的最小值已经达到最小时停止迭代
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray, np.float32(centroids), (5,5), (-1,-1), criteria)

# Now draw them
res = np.hstack((centroids,corners))
res = np.int0(res)
img[res[:,1], res[:,0]]=[0,0,255]
img[res[:,3], res[:,2]] = [0,255,0]

# 放大看图
cv2.imwrite('subpixel.jpg',img)