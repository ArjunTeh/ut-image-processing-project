import math
import cv2
import numpy as np
import seamcalculations as sc
from matplotlib import pyplot as plt

#get the image into our variables
img = cv2.imread("/home/arjun/Pictures/beach.jpg")
cv2.namedWindow("energy map", cv2.WINDOW_NORMAL)
cv2.namedWindow("original" , cv2.WINDOW_NORMAL)

seamCarver = sc.SeamCarver(img)

energy_map = seamCarver.getEnergyMap()
energy_map_norm = cv2.normalize(energy_map)
normal_em = cv2.convertScaleAbs(energy_map)

cv2.imshow("energy map", normal_em)
cv2.imshow("original", img)

newimg = img

while(cv2.getWindowProperty("original", 0) > -1):
    k = cv2.waitKey(0) & 0xFF

    if k == 27:
        cv2.destroyAllWindows()
        break
    elif k == 81:
        newimg = seamCarver.removeVerticalSeam()
        cv2.resizeWindow("energy map", newimg.shape[1], newimg.shape[0])
        cv2.imshow("energy map", newimg)
    else:
        print 'pressed: ' + str(k)
