# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pandas as pd


# define variables
alphavec=np.arange(0, 0.81, 0.01)
tauvec=[2,4,6]
rms=[]


# import the mask
mask=cv2.imread("mask_1.png", 0)


# loop throug every image
for tau in tauvec:
	for rep in range(0,4):
		for alpha in alphavec:
			alpha = round(alpha,2)
			# import cropped image
			c = 'rep_'+ str(rep)+'_tref_'+str(tau)+ '_atest_'+str(alpha)+ '_cropped.png'
			imgc = cv2.imread(c,0)
			img = cv2.bitwise_or(imgc, mask)
			
			# travel through every pixel and calculate the standard deviation 
			sd = []
			for i in range (img.shape[0]): # height of the image
				for j in range (img.shape[1]): # width of the image
					if img[i][j] != 255: # skip the white background
							sd.append(0.5885 + 514.724*img[i][j]/255)
							## Luminance = 0.5885 + 514.724*IntensityIn
							## according to the reference scale lut.scv					
			std = np.std(sd)
			rms.append([rep, alpha, tau, std])
		

# save to files
des = pd.DataFrame(rms, columns=["rep","alpha", "tau", "rmsConstrast"])
				
des.index.name = 'N'
des.to_csv("rmsContrast.csv")

