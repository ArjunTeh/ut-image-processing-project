import cv2
import numpy as np
from matplotlib import pyplot as plt

#get the image into our variables
img = cv2.imread("/home/arjun/Pictures/bird.jpg")
cv2.namedWindow("opencv")
cv2.imshow("opencv",img)

grad_img = cv2.Laplacian(img, cv2.CV_64F)

cv2.imshow("opencv", grad_img)


cv2.waitKey(0)
