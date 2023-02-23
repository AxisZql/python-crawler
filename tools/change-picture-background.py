# coding: utf-8
import numpy as np
import cv2 as cv

image = cv.imread('a.jpg')
cv.imshow("input", image)
h, w ,ch = image.shape
# 构建图像数据
data = image.reshape((-1,3))
data = np.float32(data)

# 图像分割
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
num_clusters = 4
ret,label,center=cv.kmeans(data, num_clusters, None, criteria, num_clusters, cv.KMEANS_RANDOM_CENTERS)

# 生成mask区域
index = label[0][0]
center = np.uint8(center)
color = center[0]
mask = np.ones((h, w), dtype=np.uint8)*255.
label = np.reshape(label, (h, w))
# alpha图
mask[label == index] = 0

# 下面其实就是在Photoshop中的操作
# 高斯模糊
se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
# 膨胀，防止背景出现
cv.erode(mask, se, mask)
#边缘模糊
mask = cv.GaussianBlur(mask, (5, 5), 0)
cv.imshow('alpha-image',mask)

# 白色背景
bg = np.ones(image.shape, dtype=float)*255.

# 红色背景
red = np.array([0, 0, 255])
bg_color = np.tile(red, (image.shape[0], image.shape[1], 1))

alpha = mask.astype(np.float32) / 255.
fg = alpha[..., None] * image
new_image = fg + (1 - alpha[..., None])*bg
new_image_purle = fg + (1 - alpha[..., None])*bg_color

cv.imwrite("idwhite.jpg", np.hstack((image, new_image.astype(np.uint8))))
cv.imwrite("idred.jpg", np.hstack((image, new_image_purle.astype(np.uint8))))
cv.waitKey(0)
cv.destroyAllWindows()
