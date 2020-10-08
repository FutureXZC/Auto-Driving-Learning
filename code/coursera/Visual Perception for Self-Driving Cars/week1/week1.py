import numpy as np
from cv2 import cv2
p =  [[ 640.,     0.,   640.,  2176. ],
 [   0.,   480.,   480.,   552. ],
 [   0.,     0.,     1.,     1.4]]
# print(p)
Q, R = np.linalg.qr(p)
k = R[:, 0:3]
r = np.mat(Q)
k_inv = np.linalg.inv(k)
t = - np.mat(k_inv) * np.mat(R)
t = t[:, 3]
t = np.row_stack((t, [1]))

# k, r, t, x, y, z, angle = cv2.decomposeProjectionMatrix(np.mat(p))
print(k)
print(r)
print(t)

k_left = np.row_stack((k, [0, 0, 0]))
p_left = np.column_stack((k_left, [-2., 0.25, -1.4, 1.]))
p_right = np.column_stack((k_left, [-2., -0.25, -1.4, 1.]))
p = np.linalg.inv(p_right) * p_left
print(p)