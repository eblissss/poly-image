#!/usr/bin/env python

# Ethan Bliss, October 2021

# Produces a poly-like image from an input image.
# Samples points and uses a simple implementation of marching squares.

# TODO: Export geometry so it can be rendered in 3D

import numpy as np
import cv2
import sys

# Set colors
colorA = (25, 64, 148)
colorB = (143, 157, 186)

colorThresh = 128

colorA = colorA[::-1]
colorB = colorB[::-1]

# Import image
try:
    inputImg = cv2.imread(sys.argv[1], 0)
except:
    sys.exit("Usage: marchingsquares.py [FILENAME] (X-Samples) (Y-Samples)")

# Number of samples
try:
    samplesX = int(sys.argv[2])
    samplesY = int(sys.argv[3])
except:
    samplesX = 100
    samplesY = 100
  
try:
    height, width = inputImg.shape
except:
    sys.exit("Error: File not found / incompatible")

# Step sizes
sX = width / samplesX
sY = height / samplesY


vertMatrix = np.zeros((samplesY, samplesX), dtype=np.uint8)

# Get samples
for i in range(samplesY):
    for j in range(samplesX):
        # '<' can be swapped for '>'
        if (inputImg[int(i*sY), int(j*sX)] < colorThresh):
            vertMatrix[i,j] = 1


newImg = np.full((height, width, 3), colorA, dtype=np.uint8)


#    Case 1  Case 2  Case 3  Case 4  Case 5
#                                     
#     x x     x x     x x     x o     o x
#     x x     x o     o x     x x     x x

# Do the marching (as Top-Left)
for i in range(samplesY-1):
    for j in range(samplesX-1):
        if (vertMatrix[i,j] == 1):
        
            # Case 1 - All 4 corners present
            if (vertMatrix[i,j+1] == 1 and
                vertMatrix[i+1,j] == 1 and 
                vertMatrix[i+1,j+1] == 1):
                cv2.rectangle(newImg, 
                              (int(j*sX), int(i*sY)),          # TL
                              (int((j+1)*sX), int((i+1)*sY)),  # BR
                              colorB, -1)
                              
            # Case 2 - BR missing
            elif (vertMatrix[i,j+1] == 1 and
                  vertMatrix[i+1,j] == 1):
                verts = np.array([[int(j*sX), int(i*sY)], 
                                  [int((j+1)*sX), int(i*sY)], 
                                  [int(j*sX), int((i+1)*sY)]], 
                                  np.int32)
                pts = verts.reshape((-1, 1, 2))
                cv2.fillPoly(newImg, [pts], colorB, lineType=cv2.LINE_AA)
                
            # Case 3 - BL missing
            elif (vertMatrix[i,j+1] == 1 and
                  vertMatrix[i+1,j+1] == 1):
                verts = np.array([[int(j*sX), int(i*sY)], 
                                  [int((j+1)*sX), int(i*sY)], 
                                  [int((j+1)*sX), int((i+1)*sY)]], 
                                  np.int32)
                pts = verts.reshape((-1, 1, 2))
                cv2.fillPoly(newImg, [pts], colorB, lineType=cv2.LINE_AA)
                
            # Case 4 - TR missing
            elif (vertMatrix[i+1,j] == 1 and 
                  vertMatrix[i+1,j+1] == 1):
                verts = np.array([[int(j*sX), int(i*sY)], 
                                  [int(j*sX), int((i+1)*sY)], 
                                  [int((j+1)*sX), int((i+1)*sY)]], 
                                  np.int32)
                pts = verts.reshape((-1, 1, 2))
                cv2.fillPoly(newImg, [pts], colorB, lineType=cv2.LINE_AA)
                
        # Case 5 - TL missing
        elif (vertMatrix[i,j] == 0 and 
              vertMatrix[i,j+1] == 1 and
              vertMatrix[i+1,j] == 1 and 
              vertMatrix[i+1,j+1] == 1):
            verts = np.array([[int((j+1)*sX), int(i*sY)], 
                              [int(j*sX), int((i+1)*sY)], 
                              [int((j+1)*sX), int((i+1)*sY)]], 
                              np.int32)
            pts = verts.reshape((-1, 1, 2))
            cv2.fillPoly(newImg, [pts], colorB, lineType=cv2.LINE_AA)

# Write output image
cv2.imwrite("poly" + sys.argv[1], newImg) 

