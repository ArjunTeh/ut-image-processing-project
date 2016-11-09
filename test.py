import math
import cv2
import numpy as np
import seamcalculations as sc
from matplotlib import pyplot as plt


#get the image into our variables
img = cv2.imread("/home/arjun/Pictures/bird.jpg")
cv2.namedWindow("energy map")
cv2.namedWindow("original")

seamCarver = sc.SeamCarver(img)

energy_map = seamCarver.getEnergyMap()
energy_map_norm = cv2.normalize(energy_map)
normal_em = cv2.convertScaleAbs(energy_map)

cv2.imshow("energy map", normal_em)
cv2.imshow("original", img)

newimg = img

while(True):
    k = cv2.waitKey(0) & 0xFF

    if k == 27:
        cv2.destroyAllWindows()
        break
    elif k == 81:
        newimg = seamCarver.removeVerticalSeam()
        cv2.imshow("energy map", newimg)
    else:
        print 'pressed: ' + str(k)
