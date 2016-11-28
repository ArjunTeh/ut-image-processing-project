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
        self.img = img.copy()
        self.seam_index = np.zeros(img.shape[:2])
        self.index = 0;
        self.createEnergyMap()
        self.calculateVerticalSeams()
        self.removedVSeams = []
        self.vert_seams = deque([])
        self.generatePixelMap(img)



    def generatePixelMap(self, img):
        [height, width] = img.shape[:2]
        self.pixel_map = [[0 for c in range(width)] for r in range(height)]
        for row in range(height):
            for col in range(width):
                self.pixel_map[row][col] = [row, col]




    def createEnergyMap(self):
        #calculate the gradient of the image
        blur_img = cv2.GaussianBlur(self.resized, (3, 3), 1)
        # grad_img = cv2.Laplacian(blur_img, cv2.CV_64F)
        # grad_img_abs = np.absolute(grad_img)
        sobelx = cv2.Sobel(blur_img,  cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(blur_img,  cv2.CV_64F, 0, 1, ksize=3)
        sobel_abs = cv2.addWeighted(abs(sobelx), 0.5, abs(sobely), 0.5, 0)
        #merge the channels to get the energy map
        b,g,r = cv2.split(sobel_abs)
        self.energy_map = cv2.addWeighted( cv2.addWeighted(b, 0.5, g, 0.5, 0), 0.67, r, 0.33, 0)

    #calculating seams function
    def calculateVerticalSeams(self):
        energyMap = self.energy_map
        [height, width] = energyMap.shape[:2]
        verticalSeams = np.zeros((height, width));
        verticalSeams[0,...] = energyMap[0,...]

        for rows in range(1, height):
            for cols in range(0, width):
                center = verticalSeams[rows-1, cols]
                left   = verticalSeams[rows-1, cols-1] if cols > 0 else float('inf')
                right  = verticalSeams[rows-1, cols+1] if cols < width-1 else float('inf')
                verticalSeams[rows, cols] = energyMap[rows, cols] + min(left,center,right)

        self.vertical_seam_map = verticalSeams
        return verticalSeams

    def findVerticalSeams(self):
        #find the lowest energy pixel on bottom row
        verticalSeams = self.vertical_seam_map
        [height, width] = verticalSeams.shape[:2]


        min = [float('inf'), -1]
        for i in range(0, width):
            if min[0] > verticalSeams[height-1, i]:
                min = [verticalSeams[height-1, i], i]

        #verticalSeams[height-1, min[1]] = float('inf')
        seam = [min]
        col = min[1]
        for i in range(height-2, -1, -1):
            next = [verticalSeams[i, col], col]
            if col-1 > -1:
                if verticalSeams[i, col-1] < next[0]:
                    next = [verticalSeams[i, col-1], col-1]
            if col+1 < width:
                if verticalSeams[i, col+1] < next[0]:
                    next = [verticalSeams[i, col+1], col+1]

            col = next[1]
            #verticalSeams[i, col] = float('inf')
            seam.append(next)

        self.vert_seams.append(seam)
        return seam

    def removeVerticalSeam(self):
        if not self.vert_seams:
            self.createEnergyMap()
            self.calculateVerticalSeams()
            self.findVerticalSeams()

        seam = self.vert_seams.popleft()
        [height, width] = self.resized.shape[:2]

        self.index += 1;

        for row in range(len(seam)):
            pixel = seam.pop()
            op = self.pixel_map[row][pixel[1]]
            self.seam_index[row, op[1]] = self.index
            for col in range(pixel[1], width-1):
                self.resized[row, col] = self.resized[row, col+1]
                # self.energy_map[row, col] = self.energy_map[row, col+1]
                # self.vertical_seam_map[row, col] = self.vertical_seam_map[row, col+1]
                self.pixel_map[row][col] = self.pixel_map[row][col+1]

        self.resized = np.delete(self.resized, width-1, 1)
        self.energy_map = np.delete(self.energy_map, width-1, 1)
        self.vertical_seam_map = np.delete(self.vertical_seam_map, width-1, 1)
        return self.resized

    def removeSeams(self, numSeams):
        self.index = 0
        self.seam_index = np.zeros((self.resized.shape[:2]))
        self.generatePixelMap(self.resized)
        toreturn = None
        for i in range(numSeams):
            toreturn = self.removeVerticalSeam()

        return toreturn

    def addVerticalSeam(self, numSeams):
        [height, width, depth] = self.resized.shape[:]

        addResized = cv2.copyMakeBorder(self.resized, 0,0,0,numSeams, cv2.BORDER_REPLICATE)
        self.seam_index = np.zeros((height,width))
        self.removeSeams(numSeams)

        seamResize = cv2.copyMakeBorder(self.seam_index, 0,0,0,numSeams, cv2.BORDER_REPLICATE)
        print "done calculating seams"

        for ind in range(1, numSeams+1):
            for row in range(height):
                for col in range(addResized.shape[1]-1, 0, -1):
                    addResized[row, col] = addResized[row, col-1]
                    seamResize[row, col] = seamResize[row, col-1]
                    if seamResize[row, col] == ind:
                        break
                        # addResized[row,col] += addResized[row, col+1]
                        # addResized[row,col] /= 2
                        # seamResize[row,col] = 0



        self.resized = addResized
        self.generatePixelMap(self.resized)

        return addResized


    def paintVertSeam(self):
        if not self.vert_seams:
            self.createEnergyMap()
            self.calculateVerticalSeams()
            self.findVerticalSeams()

        seamImg = self.resized.copy()

        for i in range(len(self.vert_seams)):
            seam = self.vert_seams[i]
            height = len(seam)
            for row in range(height):
                pixel = seam[height - row - 1]
                seamImg[row, pixel[1]] = [0, 0, 255]

        return seamImg

    #Getters and Setters
    def getEnergyMap(self):
        return self.energy_map
