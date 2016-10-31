import cv2
import numpy as np
from matplotlib import pyplot as plt

#get the image into our variables
img = cv2.imread("/home/arjun/Pictures/bird.jpg")
cv2.namedWindow("opencv")

#calculate the gradient of the image
grad_img = cv2.Laplacian(img, cv2.CV_64F)
grad_img_abs = np.absolute(grad_img)

#merge the channels to get the energy map
b,g,r = cv2.split(grad_img_abs)
energy_map = cv2.add( cv2.add(b, g), r)
energy_map_norm = cv2.normalize(energy_map)
normal_em = cv2.convertScaleAbs(energy_map)

print "energy_map type is " + str(type(energy_map))

cv2.imshow("opencv", normal_em)

cv2.waitKey(0)

def calculateSeams(energyMap):
    "calculates the seam energies for the energyMap given"
    return;

