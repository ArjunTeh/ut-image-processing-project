import math
import copy
import cv2
import numpy as np

class SeamCarver:
    #object variables
    #img = original image
    #energy_map = energy at each pixel
    def __init__(self, img):
        self.resized = img.copy()
        self.orig_img = img.copy()
        self.index = 0;
        self.createEnergyMap()
        self.calculateVerticalSeams()
        self.calculateHorizontalSeams()
        self.removedVSeams = []
        self.removedHSeams = []



    def createEnergyMap(self):
        #calculate the gradient of the image
        grad_img = cv2.Laplacian(self.resized, cv2.CV_64F)
        grad_img_abs = np.absolute(grad_img)
        #merge the channels to get the energy map
        b,g,r = cv2.split(grad_img_abs)
        self.energy_map = cv2.add( cv2.add(b, g), r)

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

        self.vertical_seams = verticalSeams
        return verticalSeams

    def calculateHorizontalSeams(self):
        energyMap = self.energy_map
        horizontalSeams = energyMap.copy()
        [height, width] = energyMap.shape[:2]

        for cols in range(1, width):
            for rows in range(0, height):
                center = energyMap[rows  , cols]
                below  = energyMap[rows-1, cols] if rows > 0 else float('inf')
                above  = energyMap[rows+1, cols] if rows < width-1 else float('inf')
                horizontalSeams[rows, cols] = energyMap[rows, cols] + min(above, center, below)

        self.horizontal_seams = horizontalSeams
        return horizontalSeams


    def findVerticalSeam(self):
        #find the lowest energy pixel on bottom row
        verticalSeams = self.vertical_seams
        [height, width] = verticalSeams.shape[:2]

        min = [float('inf'), -1]
        for i in range(0, width):
            if min[0] > verticalSeams[height-1, i]:
                min = [verticalSeams[height-1, i], i]

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
            seam.append(next)
        #seam should have all the horizontal indices
        #now we try to remove it.
        # print 'seam: '
        # print len(seam)
        return seam

    def findHorizontalSeam(self):
        #find the lowest energy pixel on bottom row
        horizontalSeams = self.horizontal_seams
        [height, width] = horizontalSeams.shape[:2]

        min = [float('inf'), -1]
        for i in range(0, height):
            if min[0] > horizontalSeams[i, width-1]:
                min = [horizontalSeams[i, width-1], i]

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
        #seam should have all the horizontal indices
        #now we try to remove it.
        # print 'seam: '
        # print len(seam)
        return seam


    def removeVerticalSeam(self):
        seam = self.findVerticalSeam()
        [height, width] = self.resized.shape[:2]

        self.removedVSeams.append(copy.deepcopy(seam));

        for row in range(len(seam)):
            pixel = seam.pop()
            for col in range(pixel[1], width-1):
                self.resized[row, col] = self.resized[row, col+1]
                self.energy_map[row, col] = self.energy_map[row, col+1]
                self.vertical_seams[row, col] = self.vertical_seams[row, col+1]

        self.resized = np.delete(self.resized, width-1, 1)
        self.energy_map = np.delete(self.energy_map, width-1, 1)
        self.vertical_seams = np.delete(self.vertical_seams, width-1, 1)
        return self.resized

    def removeHorizontalSeam(self):
        horiSeams = self.calculateHorizontalSeams()
        seam = self.findHorizontalSeam()
        [height, width] = self.resized.shape[:2]

        self.removedHSeams.append(copy.deepcopy(seam));

        for col in range(len(seam)):
            pixel = seam.pop()
            for row in range(pixel[1], height-1):
                self.resized[row, col] = self.resized[row+1, col]
                self.energy_map[row, col] = self.energy_map[row+1, col]

        self.resized = np.delete(self.resized, height-1, 0)
        return self.resized

    def addVerticalSeam(self):
        if (self.index < 0):
            return "can't do it right now"
        pass #push back pixels we've deleted?

    def addHorizontalSeam(self):
        if (self.index < 0):
            return "can't do it right now"
        pass #push back pixels we've deleted?

    #Getters and Setters
    def getEnergyMap(self):
        return self.energy_map
