import math
import cv2
import numpy as np

class SeamCarver:
    def __init__(self, img):
        self.resized = img.copy()
        self.orig_img = img.copy()


    def createEnergyMap(self):
        #calculate the gradient of the image
        grad_img = cv2.Laplacian(self.orig_img, cv2.CV_64F)
        grad_img_abs = np.absolute(grad_img)

        #merge the channels to get the energy map
        b,g,r = cv2.split(grad_img_abs)
        self.energy_map = cv2.add( cv2.add(b, g), r)

    #calculating seams function
    def calculateSeams(self):
        energyMap = self.energy_map
        "calculates the seam energies for the energyMap given"
        [height, width] = energyMap.shape[:2]

        verticalSeams = energyMap.copy()
        for rows in range(1, height):
            for cols in range(0, width):
                center = energyMap[rows-1, cols]
                left = energyMap[rows-1, cols-1] if cols > 0 else float('inf')
                right = energyMap[rows-1, cols+1] if cols < width-1 else float('inf')
                verticalSeams[rows, cols] = energyMap[rows, cols]

        horizontalSeams = energyMap.copy()
        for col in range(1, width):
            for rows in range(0, height):
                center = energyMap[rows-1, cols]
                above = energyMap[rows-1, cols-1] if cols > 0 else float('inf')
                below = energyMap[rows-1, cols+1] if cols < width-1 else float('inf')
                horizontalSeams[rows, cols] = energyMap[rows, cols]

        self.vertical_seams = verticalSeams
        self.horizontal_seams = horizontalSeams
        return [verticalSeams, horizontalSeams]

    def removeVerticalSeam(self):
        #find the lowest energy pixel on bottom row
        verticalMap = self.vertical_map
        [height, width] = verticalMap[:2]

        min = [float('inf'), -1]
        for i in range(width):
            if min[0] > verticalMap[height-1, i]:
                min = [verticalMap[height], i]

        seam = []
        #find the the seam
        for i in range(height):
            pass #push pixels to seam

    def removeHorizontalSeam(self):
        pass #do it

    #Getters and Setters
    def getEnergyMap(self):
        return self.energy_map
