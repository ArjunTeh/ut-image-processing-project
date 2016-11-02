import math
import cv2
import numpy as np

#calculating seams function
def calculateSeams(energyMap):
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

    return [verticalSeams, horizontalSeams]
