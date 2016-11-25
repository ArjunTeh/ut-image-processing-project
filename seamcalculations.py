import math
import copy
import cv2
import numpy as np
from collections import deque

class SeamCarver:
    #object variables
    #img = original image
    #energy_map = energy at each pixel
    def __init__(self, img, cachesize):
        self.seam_cache_size = cachesize
        self.resized = img.copy()
        self.orig_img = img.copy()
        self.index = 0;
        self.createEnergyMap()
        self.calculateVerticalSeams()
        self.calculateHorizontalSeams()
        self.removedVSeams = []
        self.removedHSeams = []
        self.vert_seams = deque([])
        self.hori_seams = deque([])



    def createEnergyMap(self):
        #calculate the gradient of the image
        blur_img = cv2.GaussianBlur(self.resized, (3, 3), 1)
        grad_img = cv2.Laplacian(blur_img, cv2.CV_64F)
        grad_img_abs = np.absolute(grad_img)
        sobelx = cv2.Sobel(blur_img,  cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(blur_img,  cv2.CV_64F, 0, 1, ksize=3)
        sobel_abs = cv2.addWeighted(abs(sobelx), 0.5, abs(sobely), 0.5, 0)
        #merge the channels to get the energy map
        b,g,r = cv2.split(sobel_abs)
        self.energy_map = cv2.addWeighted( cv2.addWeighted(b, 0.5, g, 0.5, 0), 0.67, r, 0.33, 0)

    #calculating seams function
    def calculateVerticalSeams(self):
        energyMap = self.energy_map
        verticalSeams = energyMap.copy()
        [height, width] = energyMap.shape[:2]

        for rows in range(1, height):
            for cols in range(0, width):
                center = energyMap[rows-1, cols]
                left   = energyMap[rows-1, cols-1] if cols > 0 else float('inf')
                right  = energyMap[rows-1, cols+1] if cols < width-1 else float('inf')
                verticalSeams[rows, cols] = energyMap[rows, cols] + min(left,center,right)

        self.vertical_seam_map = verticalSeams
        return verticalSeams

    def calculateHorizontalSeams(self):
        energyMap = self.energy_map
        horizontalSeams = energyMap.copy()
        [height, width] = energyMap.shape[:2]

        for cols in range(1, width):
            for rows in range(0, height):
                center = energyMap[rows  , cols]
                if rows > 0:
                    below = energyMap[rows-1, cols]
                else:
                    below = float('inf')
                if rows < height-1:
                    above = energyMap[rows+1, cols]
                else:
                    above = float('inf')
                horizontalSeams[rows, cols] = energyMap[rows, cols] + min(above, center, below)

        self.horizontal_seam_map = horizontalSeams
        return horizontalSeams


    def findVerticalSeams(self, num_seams):
        #find the lowest energy pixel on bottom row
        verticalSeams = self.vertical_seam_map
        [height, width] = verticalSeams.shape[:2]

        for bleh in range(num_seams):
            min = [float('inf'), -1]
            for i in range(0, width):
                if min[0] > verticalSeams[height-1, i]:
                    min = [verticalSeams[height-1, i], i]

            verticalSeams[height-1, min[1]] = float('inf')
            seam = [min]
            col = min[1]
            for i in range(height-1, 0, -1):
                next = [verticalSeams[i, col], col]
                if col-1 > 0:
                    if verticalSeams[i, col-1] < next[0]:
                        next = [verticalSeams[i, col-1], col-1]
                if col+1 < width:
                    if verticalSeams[i, col+1] < next[0]:
                        next = [verticalSeams[i, col+1], col+1]

                col = next[1]
                #verticalSeams[i, col] = float('inf')
                seam.append(next)

            self.vert_seams.append(seam)

        return self.vert_seams

    def findHorizontalSeams(self, num_seams):
        #find the lowest energy pixel on bottom row
        horizontalSeams = self.horizontal_seam_map
        [height, width] = horizontalSeams.shape[:2]

        for bleh in range(num_seams):
            min = [float('inf'), -1]
            for i in range(0, height):
                if min[0] > horizontalSeams[i, width-1]:
                    min = [horizontalSeams[i, width-1], i]

            horizontalSeams[min[1], width-1] = float('inf')
            seam = [min]
            row = min[1]
            for i in range(width-1, 0, -1):
                next = [horizontalSeams[row, i], row]
                if row-1 > 0:
                    if horizontalSeams[row-1, i] < next[0]:
                        next = [horizontalSeams[row-1, i], row-1]
                if row+1 < width:
                    if horizontalSeams[row+1, i] < next[0]:
                        next = [horizontalSeams[row+1, i], row+1]

                row = next[1]
                seam.append(next)

            self.hori_seams.append(seam)

        return self.hori_seams


    def removeVerticalSeam(self):
        if not self.vert_seams:
            self.createEnergyMap()
            self.calculateVerticalSeams()
            self.findVerticalSeams(self.seam_cache_size)

        seam = self.vert_seams.popleft()
        [height, width] = self.resized.shape[:2]

        self.removedVSeams.append(copy.deepcopy(seam));

        for row in range(len(seam)):
            pixel = seam.pop()
            for col in range(pixel[1], width-1):
                self.resized[row, col] = self.resized[row, col+1]
                self.energy_map[row, col] = self.energy_map[row, col+1]
                self.vertical_seam_map[row, col] = self.vertical_seam_map[row, col+1]

        self.resized = np.delete(self.resized, width-1, 1)
        self.energy_map = np.delete(self.energy_map, width-1, 1)
        self.vertical_seam_map = np.delete(self.vertical_seam_map, width-1, 1)
        return self.resized

    def removeHorizontalSeam(self):
        if not self.hori_seams:
            self.createEnergyMap()
            self.calculateHorizontalSeams()
            self.findHorizontalSeams(self.seam_cache_size)

        seam = self.hori_seams.popleft()
        [height, width] = self.resized.shape[:2]

        self.removedHSeams.append(copy.deepcopy(seam));

        for col in range(len(seam)):
            pixel = seam.pop()
            for row in range(pixel[1], height-1):
                self.resized[row, col] = self.resized[row+1, col]
                self.energy_map[row, col] = self.energy_map[row+1, col]
                self.horizontal_seam_map[row, col] = self.horizontal_seam_map[row+1,col]

        self.resized = np.delete(self.resized, height-1, 0)
        self.energy_map = np.delete(self.energy_map, height-1, 0)
        self.horizontal_seam_map = np.delete(self.horizontal_seam_map, height-1, 0)
        return self.resized

    def addVerticalSeam(self):
        if not self.vert_seams:
            self.createEnergyMap()
            self.findVerticalSeams(10)

        seam = self.vert_seams.popleft()
        [height, width] = self.resized.shape[:2]
        addResized = np.append(self.resized, np.zeros((height, 1, 3)), axis=1)
        addEnergy = np.append(self.resized, np.zeros((height, 1, 3)), axis=1)

        for row in range(len(seam)):
            pixel = seam.pop()
            for col in range(width-1, pixel[1], -1):
                addResized[row, col] = self.resized[row, col-1]
                addEnergy[row, col] = self.energy_map[row, col-1]

            addResized[row, pixel[1]] = (addResized[row, pixel[1]-1] + addResized[row, pixel[1]+1])/2

        self.resized = addResized
        self.energy_map = addEnergy

        return self.resized

    def addHorizontalSeam(self):
        if (self.index < 0):
            return "can't do it right now"
        pass #push back pixels we've deleted?

    #Getters and Setters
    def getEnergyMap(self):
        return self.energy_map
