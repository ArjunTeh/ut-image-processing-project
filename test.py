import sys
import math
import cv2
import numpy as np
import seamcalculations as sc
from matplotlib import pyplot as plt


#helper functions
def showEnergyMap():
    energy_map = seamCarver.seam_index#getEnergyMap()
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

scale = 1

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
        cv2.resizeWindow("seam carved", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
        cv2.resizeWindow("original", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
        cv2.imshow("seam carved", newimg)
        showEnergyMap()
    elif k == 83:
        newimg = seamCarver.addVerticalSeam(50)
        cv2.resizeWindow("seam carved", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale))
        cv2.resizeWindow("original", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale))
        cv2.imshow("seam carved", newimg)
    elif k == 61:
        scale += 0.2
        cv2.resizeWindow("seam carved", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
        cv2.resizeWindow("original", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
    elif k == 45:
        scale -= 0.2
        cv2.resizeWindow("seam carved", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
        cv2.resizeWindow("original", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
    else:
        print 'pressed: ' + str(k)
