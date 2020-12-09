# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pandas as pd

alphavec = np.arange(0, 0.51, 0.01)
tau = 2.8

for rep in range(0,5):
	sdvec = []
	for alpha in alphavec:
		alpha = round(alpha,2)
		# import image
		m = 'mask_1.png'
		f = 'rep_'+str(rep)+'_aref_0.05_tref_'+str(tau)+'_atest_'+str(alpha)+'.png'
		src1 = cv2.imread(f,0)
		src2 = cv2.imread(m,0)


		# crop the foreground
		img = cv2.bitwise_or(src1,src2)



		# compute sd of all pixels 
		sd = []
		for i in range (img.shape[0]): #traverses through height of the image
			for j in range (img.shape[1]): #traverses through width of the image
				if img[i][j] == 255:
					img[i][j] = 142
					
				else:
					#print(img[i][j])
					sd.append(img[i][j])

		sd = np.std(sd)
		std = round(sd, 1)
		sdvec.append(sd)
		#print(sdvec)
		
		print(std)
		cv2.imwrite('rep_'+str(rep)+'_aref_0.05_tref_'+str(tau)+'_atest_'+str(alpha)+'.png', src1)
		cv2.imwrite("rep_"+str(rep)+"_aref_0.05_tref_"+str(tau)+"_atest_"+str(alpha)+"_cropped.png", img)

	#print(alphavec.shape)
	#print(sdvec)

	d = np.row_stack((alphavec, sdvec))
	d = np.transpose(d)

	des = pd.DataFrame(d, columns=["alpha", "rmsConstrast"])
			
	des.index.name = 'N'
	des.to_csv("rep_"+str(rep)+"_tref_"+str(tau)+"_rmsContrast.csv")


