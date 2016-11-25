import sys
import math
import cv2
import numpy as np
import seamcalculations as sc
from matplotlib import pyplot as plt


#helper functions
def showEnergyMap():
    energy_map = seamCarver.getEnergyMap()
    energy_map_norm = cv2.normalize(energy_map)
    normal_em = cv2.convertScaleAbs(energy_map)
    normal_em = cv2.applyColorMap(normal_em, cv2.COLORMAP_JET)
    cv2.imshow("energy map", normal_em)


if(len(sys.argv) != 3):
    print "please include just one input file"
    sys.exit(2)

filename = sys.argv[2]
cachesize = int(float(sys.argv[1]))

#get the image into our variables
img = cv2.imread(filename)
cv2.namedWindow("energy map")
cv2.namedWindow("seam carved", cv2.WINDOW_NORMAL)
cv2.namedWindow("original" , cv2.WINDOW_NORMAL)

seamCarver = sc.SeamCarver(img, cachesize)

energy_map = seamCarver.getEnergyMap()
energy_map_norm = cv2.normalize(energy_map)
normal_em = cv2.convertScaleAbs(energy_map)
normal_em = cv2.applyColorMap(normal_em, cv2.COLORMAP_JET)

cv2.imshow("energy map", normal_em)
cv2.imshow("seam carved", img)
cv2.imshow("original", img)

newimg = img

while(cv2.getWindowProperty("original", 0) > -1):
    k = cv2.waitKey(0) & 0xFF

    if k == 27:
        cv2.destroyAllWindows()
        break
    elif k == 81:
        seamimg = seamCarver.paintVertSeam()
        newimg = seamCarver.removeVerticalSeam()
        cv2.imshow("seam carved", seamimg)
        cv2.waitKey(1000) & 0xFF
        cv2.resizeWindow("seam carved", newimg.shape[1], newimg.shape[0])
        cv2.resizeWindow("original", newimg.shape[1], newimg.shape[0])
        cv2.imshow("seam carved", newimg)
        showEnergyMap()
    elif k == 83:
        newimg = seamCarver.addVerticalSeam()
        cv2.resizeWindow("seam carved", newimg.shape[1], newimg.shape[0])
        cv2.resizeWindow("original", newimg.shape[1], newimg.shape[0])
        cv2.imshow("seam carved", newimg)
    elif k == 82:
        newimg = seamCarver.removeHorizontalSeam()
        cv2.resizeWindow("seam carved", newimg.shape[1], newimg.shape[0])
        cv2.resizeWindow("original", newimg.shape[1], newimg.shape[0])
        cv2.imshow("seam carved", newimg)
    elif k == 84:
        newimg = seamCarver.addHorizontalSeam()
        pass
    # elif k == 104:
    #     curimg = seamCarver.resized
    #     for i in range(curimg.shape[0]/2):
    #         seamCarver.removeHorizontalSeam()
    #     for i in range(curimg.shape[1]/2):
    #         seamCarver.removeVerticalSeam()
    #     curimg = seamCarver.resized
    #     cv2.resizeWindow("seam carved", curimg.shape[1], curimg.shape[0])
    #     cv2.imshow("seam carved", curimg)
    else:
        print 'pressed: ' + str(k)
