#!/usr/bin/env python

# Ethan Bliss, Nov. 2021

# Produces a poly-like image from an input image.
# Samples points and uses a simple implementation of marching squares.

# TODO: Export geometry so it can be rendered in 3D (obj file)

import numpy as np
import cv2
import sys

def main():
    # Set colors
    colorA = (25, 64, 148)
    colorB = (143, 157, 186)
    colorA = colorA[::-1]
    colorB = colorB[::-1]

    colorThresh = 128

    # Import image
    try:
        inputImg = cv2.imread(sys.argv[1], 0)
    except:
        sys.exit("Usage: polyimage.py [FILENAME] (X-Samples) (Y-Samples)")

    # Number of samples
    try:
        samplesX = int(sys.argv[2])
        samplesY = int(sys.argv[3])
    except:
        samplesX = 100
        samplesY = 100
    
    # Get image shape
    try:
        height, width = inputImg.shape
    except:
        sys.exit("Error: File not found / incompatible")

    # Step sizes
    stepX = width / samplesX
    stepY = height / samplesY

    verts = sampleImage(samplesX, samplesY, stepX, stepY, colorThresh, inputImg)

    # Override output size
    height *= 2
    width *= 2
    stepX *= 2
    stepY *= 2

    # Initialize output image
    newImg = np.full((height, width, 3), colorA, dtype=np.uint8)

    # March
    #simpleMarch(samplesX, samplesY, stepX, stepY, verts, newImg, colorB)
    imageMarch(samplesX, samplesY, stepX, stepY, verts, newImg, colorB)
    
    # Write output image
    cv2.imwrite("poly" + sys.argv[1], newImg) 


# Sample the image at designated steps
def sampleImage(samplesX, samplesY, stepX, stepY, colorThresh, inputImg):
    # v is the Vertice Matrix
    v = np.full((samplesY, samplesX), False)

    # Get samples
    for i in range(samplesY):
        for j in range(samplesX):
            # '<' can be swapped for '>'
            if (inputImg[int((i+0.5)*stepY), int((j+0.5)*stepX)] < colorThresh):
                v[i,j] = True
    
    return v

# Produce a new image from given vertices
def imageMarch(samplesX, samplesY, sX, sY, v, newImg, colorB):
    # Cases from https://en.wikipedia.org/wiki/Marching_squares
    #
    #   Case 0  Case 1  Case 2  Case 3  Case 4  Case 5
    #    o o     o o     o o     o o     o x     o x
    #    o o     x o     o x     x x     o o     x o
    #
    #   Case 6  Case 7  Case 8  Case 9  Case 10 Case 11
    #    o x     o x     x o     x o     x o     x o
    #    o x     x x     o o     x o     o x     x x
    #
    #   Case 12 Case 13 Case 14 Case 15
    #    x x     x x     x x     x x
    #    o o     x o     o x     x x 
    #
    case = 0
    vertArray = np.empty((0,2))
    # Do the marching (as Top-Left)
    for i in range(samplesY-1):
        for j in range(samplesX-1):
            # Find the case
            if not v[i,j]:
                if not v[i,j+1]:
                    if not v[i+1,j+1]:
                        if not v[i+1,j]:
                            case = 0
                        else:
                            case = 1
                    else:
                        if not v[i+1,j]:
                            case = 2
                        else:
                            case = 3
                else:
                    if not v[i+1,j+1]:
                        if not v[i+1,j]:
                            case = 4
                        else:
                            case = 5
                    else:
                        if not v[i+1,j]:
                            case = 6
                        else:
                            case = 7
            else:
                if not v[i,j+1]:
                    if not v[i+1,j+1]:
                        if not v[i+1,j]:
                            case = 8
                        else:
                            case = 9
                    else:
                        if not v[i+1,j]:
                            case = 10
                        else:
                            case = 11
                else:
                    if not v[i+1,j+1]:
                        if not v[i+1,j]:
                            case = 12
                        else:
                            case = 13
                    else:
                        if not v[i+1,j]:
                            case = 14
                        else:
                            case = 15

            # Get verts
            if case == 0:
                pass
            elif case == 1:
                verts = np.array([[j, i+0.5],
                                  [j, i+1],
                                  [j+0.5, i+1]])                
            elif case == 2:
                verts = np.array([[j+0.5, i+1], 
                                  [j+1, i+1],
                                  [j+1, i+0.5]])
            elif case == 3:
                verts = np.array([[j, i+0.5], 
                                  [j, i+1],
                                  [j+1, i+1],
                                  [j, i+0.5],
                                  [j+1, i+1],
                                  [j+1, i+0.5]])
            elif case == 4:
                verts = np.array([[j+0.5, i], 
                                  [j+1, i+0.5],
                                  [j+1, i]])
            elif case == 5:
                verts = np.array([[j, i+0.5], 
                                  [j, i+1],
                                  [j+0.5, i+1],
                                  [j+0.5, i], 
                                  [j+1, i+0.5],
                                  [j+1, i],
                                  [j, i+0.5], 
                                  [j+0.5, i+1],
                                  [j+0.5, i],
                                  [j+0.5, i],
                                  [j+0.5, i+1],
                                  [j+1, i+0.5]]) 
            elif case == 6:
                verts = np.array([[j+0.5, i], 
                                  [j+0.5, i+1],
                                  [j+1, i+1],
                                  [j+0.5, i], 
                                  [j+1, i+1],
                                  [j+1, i]])
            elif case == 7:
                verts = np.array([[j, i+0.5],
                                  [j+1, i+0.5],
                                  [j+0.5, i],
                                  [j+0.5, i],
                                  [j+1, i+0.5],
                                  [j+1, i],
                                  [j, i+0.5], 
                                  [j, i+1],
                                  [j+1, i+1],
                                  [j, i+0.5],
                                  [j+1, i+1],
                                  [j+1, i+0.5]])
            elif case == 8:
                verts = np.array([[j, i], 
                                  [j, i+0.5],
                                  [j+0.5, i]])
            elif case == 9:
                verts = np.array([[j, i], 
                                  [j, i+1],
                                  [j+0.5, i+1],
                                  [j, i], 
                                  [j+0.5, i+1],
                                  [j+0.5, i]])
            elif case == 10:
                verts = np.array([[j, i], 
                                  [j, i+0.5],
                                  [j+0.5, i],
                                  [j+0.5, i+1], 
                                  [j+1, i+1],
                                  [j+1, i+0.5],
                                  [j, i+0.5], 
                                  [j+0.5, i+1],
                                  [j+0.5, i],
                                  [j+0.5, i],
                                  [j+0.5, i+1],
                                  [j+1, i+0.5]])
            elif case == 11:
                verts = np.array([[j, i], 
                                  [j, i+0.5],
                                  [j+0.5, i],
                                  [j, i+0.5],
                                  [j+1, i+0.5],
                                  [j+0.5, i],
                                  [j, i+0.5], 
                                  [j, i+1],
                                  [j+1, i+1],
                                  [j, i+0.5],
                                  [j+1, i+1],
                                  [j+1, i+0.5]])
            elif case == 12:
                verts = np.array([[j, i], 
                                  [j, i+0.5],
                                  [j+1, i+0.5],
                                  [j, i],
                                  [j+1, i+0.5],
                                  [j+1, i]])
            elif case == 13:
                verts = np.array([[j, i], 
                                  [j, i+0.5],
                                  [j+1, i+0.5],
                                  [j, i],
                                  [j+1, i+0.5],
                                  [j+1, i],
                                  [j, i+0.5],
                                  [j, i+1],
                                  [j+0.5, i+1],
                                  [j, i+0.5],
                                  [j+0.5, i+1],
                                  [j+1, i+0.5]])
            elif case == 14:
                verts = np.array([[j, i], 
                                  [j, i+0.5],
                                  [j+1, i+0.5],
                                  [j, i],
                                  [j+1, i+0.5],
                                  [j+1, i],
                                  [j, i+0.5],
                                  [j+0.5, i+1],
                                  [j+1, i+0.5],
                                  [j+0.5, i+1],
                                  [j+1, i+1],
                                  [j+1, i+0.5]])
            elif case == 15:
                verts = np.array([[j+0.0, i],
                                  [j, i+1],
                                  [j+1, i+1],
                                  [j, i],
                                  [j+1, i+1],
                                  [j+1, i]])
            
            # Draw verts
            if case != 0:
                vertArray = np.append(vertArray, verts, axis=0)
                verts[:,0] *= sX
                verts[:,1] *= sY
                for tri in np.split(verts, len(verts) / 3):
                    tri = tri.reshape((-1, 1, 2)).astype(int)
                    cv2.fillPoly(newImg, [tri], colorB, lineType=cv2.LINE_AA)

    #createObj(vertArray)
    

### Idea for making *efficient* obj file
# 1. Go over all verts and add to hash table (dict) if new
#    i. If new, give new index and add
#    ii. If old, nothing
# 2. Go through hash table and add to obj file as verts
# 3. Use hash table lookup to add faces
def createObj(vertArray):
    
    vertDict = {}
    for point in vertArray:
        tp = tuple(point)
        if tp not in vertDict:
            vertDict[tp] = 0
    
    for i, point in enumerate(vertDict):
        vertDict[point] = i
        # Write points to file

    for i in len(vertArray / 3):
        #Write to file: (vertDict[i*3], vertDict[i*3+1], vertDict[i*3+2])
        pass



def simpleMarch(samplesX, samplesY, sX, sY, v, newImg, colorB):
    #    Case 1  Case 2  Case 3  Case 4  Case 5
    #                                     
    #     x x     x x     x x     x o     o x
    #     x x     x o     o x     x x     x x

    # Do the marching (as Top-Left)
    for i in range(samplesY-1):
        for j in range(samplesX-1):
            case = 0
            if v[i,j]:
                if v[i,j+1]:
                    if v[i+1,j]:
                        if v[i+1,j+1]:
                            case = 1
                        else:
                            case = 2
                    else:
                        if v[i+1, j+1]:
                            case = 3
                else:
                    if v[i+1,j]:
                        if v[i+1,j+1]:
                            case = 4
            else:
                if v[i,j+1]:
                    if v[i+1,j]:
                        if v[i+1,j+1]:
                            case = 5

            # Get verts
            if case == 1:
                verts = np.array([[j, i],
                                  [j, i+1],
                                  [j+1, i+1],
                                  [j, i],
                                  [j+1, i+1],
                                  [j+1, i]])
            elif case == 2:
                verts = np.array([[j, i], 
                                  [j, i+1], 
                                  [j+1, i]])
            elif case == 3:
                verts = np.array([[j, i], 
                                  [j+1, i+1], 
                                  [j+1, i]])
            elif case == 4:
                verts = np.array([[j, i], 
                                  [j, i+1], 
                                  [j+1, i+1]])
            elif case == 5:
                verts = np.array([[j, i+1], 
                                  [j+1, i+1], 
                                  [j+1, i]])

            # Draw verts
            if case != 0:
                #vertArray = np.append(vertArray, verts, axis=0)
                verts = verts.astype(float)
                verts[:,0] *= sX
                verts[:,1] *= sY
                for tri in np.split(verts, len(verts) / 3):
                    tri = tri.reshape((-1, 1, 2)).astype(int)
                    cv2.fillPoly(newImg, [tri], colorB, lineType=cv2.LINE_AA)


if __name__ == "__main__":
    main()