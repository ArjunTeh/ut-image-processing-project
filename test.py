import math
import cv2
import numpy as np
from seamcalculations import calculateSeams
from matplotlib import pyplot as plt


#get the image into our variables
img = cv2.imread("/home/arjun/Pictures/bird.jpg")
cv2.namedWindow("energy map")
cv2.namedWindow("original")

#calculate the gradient of the image
grad_img = cv2.Laplacian(img, cv2.CV_64F)
grad_img_abs = np.absolute(grad_img)

#merge the channels to get the energy map
b,g,r = cv2.split(grad_img_abs)
energy_map = cv2.add( cv2.add(b, g), r)
energy_map_norm = cv2.normalize(energy_map)
normal_em = cv2.convertScaleAbs(energy_map)

print energy_map.shape

calculateSeams(energy_map)

cv2.imshow("energy map", normal_em)
cv2.imshow("original", img)

while(True):
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
    else:
        print k
