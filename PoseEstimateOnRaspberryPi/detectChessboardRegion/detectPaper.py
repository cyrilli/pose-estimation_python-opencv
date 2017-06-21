# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 09:12:34 2016

@author: li_ch

detect paper in an image
"""
# import the necessary packages

import numpy as np

import cv2
 

image = cv2.imread('H:/blackEdge/1465780496_white.jpg')

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
 
# show the original image and the edge detected image
print "STEP 1: Edge Detection"
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite('H:/origin.jpg',image)
#cv2.imwrite('H:/edged.jpg',edged)
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
 
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
 
# show the contour (outline) of the piece of paper
print "STEP 2: Find contours of paper"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite('H:/outline.jpg',image)

# show the mask of the piece of paper
mask = np.zeros(gray.shape,np.uint8)
cv2.drawContours(mask,[screenCnt],0,255,-1)
cv2.imshow('mask',mask),cv2.waitKey(0),cv2.destroyAllWindows()
#cv2.imwrite('H:/mask.jpg',mask)
mask = mask/255
result = image.copy()
result[:,:,0] = result[:,:,0]*mask
result[:,:,1] = result[:,:,1]*mask
result[:,:,2] = result[:,:,2]*mask
cv2.imshow('without background',result),cv2.waitKey(0),cv2.destroyAllWindows()
cv2.imwrite('H:/white.jpg',result)