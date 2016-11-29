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


drawing = False # true if mouse is pressed
ix, ex = -1,-1

def updateBounds(x):
    global ix, ex
    if x < ix:
        ix = x
    elif ix < 0:
        ix = x
    if x+10 > ex:
        ex = x+10


def draw_rect(event, x,y, flags, param):
    global drawing, ix, ex
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.rectangle(blank, (x,y), (x+10,y+10), (0,255,0), -1)
        updateBounds(x)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.rectangle(blank, (x,y), (x+10,y+10), (0,255,0), -1)
            updateBounds(x)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    bleh = cv2.addWeighted(seamCarver.resized, 1.0, blank, 0.3, 0)
    cv2.imshow("seam carved", bleh)


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

cv2.setMouseCallback("seam carved", draw_rect)

seamCarver = sc.SeamCarver(img, cachesize)

energy_map = seamCarver.getEnergyMap()
energy_map_norm = cv2.normalize(energy_map)
normal_em = cv2.convertScaleAbs(energy_map)
normal_em = cv2.applyColorMap(normal_em, cv2.COLORMAP_JET)

cv2.imshow("energy map", normal_em)
cv2.imshow("seam carved", img)
cv2.imshow("original", img)

#add blank img for drawing
blank = cv2.convertScaleAbs(np.zeros(img.shape))


newimg = img

scale = 1

while(cv2.getWindowProperty("original", 0) > -1):
    k = cv2.waitKey(0) & 0xFF

    if k == 27:
        break
    elif k == 81:
        seamimg = seamCarver.paintVertSeam()
        newimg = seamCarver.removeSeams(1)
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
    elif k == 100:
        #delete the object from the scene
        objWidth = ex - ix + 1
        newimg = seamCarver.removeSelection(blank[:,:,1], objWidth)
        blank = cv2.convertScaleAbs(np.zeros(seamCarver.resized.shape))
    elif k == 61:
        scale += 0.2
        cv2.resizeWindow("seam carved", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
        cv2.resizeWindow("original", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
    elif k == 45:
        scale -= 0.2
        cv2.resizeWindow("seam carved", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
        cv2.resizeWindow("original", int(newimg.shape[1]*scale), int(newimg.shape[0]*scale) )
    elif k == 99:
        blank = cv2.convertScaleAbs(np.zeros(seamCarver.resized.shape))
        showEnergyMap()

    else:
        print 'pressed: ' + str(k)

cv2.destroyAllWindows()
