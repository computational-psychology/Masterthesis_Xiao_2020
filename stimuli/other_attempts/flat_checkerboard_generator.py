# -*- coding: utf-8 -*-
"""
verigated checkerboard generator

"""

import numpy as np
import cv2
import random
import pandas as pd



S = 144 # number of grids
N = 13 # number of colors
# thirteen reflectance values as in Wiebel, Aguilar and Maertens 2017
# reflectances = np.array([0.06, 0.11, 0.19, 0.31, 0.46, 0.63, 0.82, 1.05, 1.29, 1.50, 1.67, 1.95, 2.22])

# thirteen RGB grey values with a mean of 127.5
cls =  np.linspace(0,255,num = N)

# create a black image
img = np.zeros((512,512,3), np.uint8)
picked_color = {}
# draw rectangles
for i in range(S):
	for j in range(S):
		non_possible = []
		if i != 0:
			non_possible.append(picked_color[(i-1, j)])
		if j != 0:
			non_possible.append(picked_color[(i, j-1)])
		k = i+1
		l = j+1
		random.shuffle(cls)	
		while cls[0] in non_possible:
			random.shuffle(cls)
		picked_color[(i,j)] = cls[0]
		cv2.rectangle(img,(i*512//S,j*512//S),(k*512//S,l*512//S),(cls[0],cls[0],cls[0]),-1)

cv2.imshow('ckb',img)
cv2.waitKey()

cv2.imwrite("vgckb.png", img)
ckb = cv2.imread("vgckb.png")
	
# draw a circle
cc = cv2.circle(img,(256,256), 75, (110,110,110), -1)
dst= cv2.addWeighted(ckb,0.39,cc,0.9,0) #black:100, white:200 in the center


# create a mask image with a white circle
mask = np.zeros((512,512,3), np.uint8)
mask = cv2.circle(mask,(256,256), 75, (255,255,255), -1)
mask = cv2.bitwise_not(mask)

# crop the foreground & cut the circular part of dst
fg = cv2.bitwise_or(dst,mask)


# place it on the original checkerboard with a circle in the center
cckb = cv2.circle(img,(256,256), 75, (255,255,255), -1)
fckb = cv2.bitwise_and(cckb,fg)

# put it on a grey backgroud
# create a background
bg = np.full((512, 512, 3), 127, np.uint8) 
bg = cv2.circle(bg,(256,256), 75, (255,255,255), -1)
# combine them
mckb = cv2.bitwise_and(bg,fg)


cv2.imshow('fckb',fckb)
#cv2.imshow('mckb',mckb)
cv2.waitKey() 

# write the image
cv2.imwrite("full_vg_" + str(S) + ".png", fckb)



