# -*- coding: utf-8 -*-
"""
Created on Thu May  7 14:39:16 2020

This is a script for adding noise to checkerboards


@author: Yiqun
"""

import numpy as np
import cv2
import random

color_white = 255
color_black = 0
m_file_name = "mask_checkerboard.png" 
crop_mask_name = "mask_crop.png"


# backround noise generator
def cci_background(n_grid,n_image_size,f_file_name):
	# n_grid: number of rectangles to be created
	# n_image_size: size of the background image in pixel
	# n_grid must be a sivisor of n_image_size
	# f_file_name: name of the file to be created

	
	# create a black background
	img = np.zeros((n_image_size,n_image_size,3), np.uint8)
	
	# prepare colors that would be later fill into rectangles
	colors = np.array([color_black,color_white])
		
	
	# draw black or white rectangles on the black background
	for i in range(n_grid):
		for j in range(n_grid):
			random.shuffle(colors)
			color = int(colors[0])
			cv2.rectangle(img,(i*n_image_size//n_grid,j*n_image_size//n_grid),
					((i+1)*n_image_size//n_grid,(j+1)*n_image_size//n_grid),
					(color,color,color),-1)
	#cv2.imshow('contrast contrast illusion - background',img)
	#cv2.waitKey()
	# write the image
	cv2.imwrite(f_file_name,img)
	return





def uncovered_noised_checkerboard(f_file_name,m_file_name,c_file_name,
								  n_image_size,n_weight,color_background):
	# f_file_name: name of the background noise
	# m_file_name: name of the mask
	# c_file_name: name of the checkerboard
	# n_weight: weight of the noise in alpha blending
	
	
	# read images
	noise_background = cv2.imread(f_file_name)
	mask = cv2.imread(m_file_name)# the mask is created in photoshop
	checkerboard = cv2.imread(c_file_name)
	
	# crop the noise background and free the checkerboard from its background
	noise_masked = cv2.bitwise_or(noise_background,mask)
	checkerboard_masked= cv2.bitwise_or(checkerboard,mask)
	#cv2.imshow('n_m',noise_masked)
	#cv2.imshow('ckb_m',checkerboard_masked)
	#cv2.waitKey()
	
	# add noise to the checkerboard
	noised_checkerboard = cv2.addWeighted(noise_masked,n_weight,checkerboard_masked,1-n_weight,0)
	#cv2.imshow('noised_checkerboard',noised_checkerboard)
	#cv2.waitKey()
	
	# creat a grey background and place the noised checkerboard in
	grey_background = np.full((n_image_size, n_image_size, 3), color_background, np.uint8)
	background_mask = cv2.bitwise_not(mask)
	grey_background_masked = cv2.bitwise_or(background_mask,grey_background)
	checkerboard_masked_grey = cv2.bitwise_and(grey_background_masked,noised_checkerboard)
	
	#cv2.imshow('checkerboard_masked_grey',checkerboard_masked_grey)
	#cv2.waitKey()
	
	# save the file
	checkerboard_masked_file_name = "uncovered_noised_checkerboard_"
	n_weight_file_name = "_weight_" + str(n_weight)
	checkerboard_noise_file_name = checkerboard_masked_file_name + n_weight_file_name + ".png"
	cv2.imwrite(checkerboard_noise_file_name,checkerboard_masked_grey)
	
	return checkerboard_masked_grey



def add_transparent_layer(color_trans, alpha_weight):
	# color_trans: color of the transparent layer [0,255]
	# alpha_weight: transparency of the transparent layer [0,1]
	noised_checkerboard = uncovered_noised_checkerboard(f_file_name,m_file_name,c_file_name,
									  n_image_size,n_weight,color_background)
	checkerboard = uncovered_noised_checkerboard(f_file_name,m_file_name,c_file_name,
									  n_image_size,n_weight,color_background)
	
	# creat a non-transparent cover
	start_point = (174, 361) # measured from the original stimulus
	end_point = (425,532) # measured from the original stimulus
	color = (color_trans, color_trans, color_trans) 
	thickness = -1 # fill rectangle
	checkerboard_cover = cv2.rectangle(noised_checkerboard,start_point, end_point, 
											  color, thickness)
	
	# add transparency
	checkerboard_trans = cv2.addWeighted(checkerboard_cover,
										 1-alpha_weight,checkerboard,alpha_weight,0)
	#cv2.imshow('noised_checkerboard_trans',checkerboard_trans)
	#cv2.waitKey()
	
	checkerboard_trans_file_name = "noised_checkerboard" + "_weight_" + str(n_weight) + "_alpha_" + str(alpha_weight) + "_ref_" + str(color_trans) + ".png"
	cv2.imwrite(checkerboard_trans_file_name,checkerboard_trans)
	return checkerboard_trans



# crop the masked checkerboard
def crop_checkerboard(color_trans,alpha_weight,crop_mask_name,n_image_size,color_background):
	checkerboard_trans = add_transparent_layer(color_trans, alpha_weight)
	mask_crop = cv2.imread(crop_mask_name)# the mask is created in photoshop
	checkerboard_cropped = cv2.bitwise_or(checkerboard_trans,mask_crop)
	
	# creat a grey background and place the cropped checkerboard in
	mask_background = cv2.bitwise_not(mask_crop)# the mask for the background
	grey_background = np.full((n_image_size, n_image_size, 3), color_background, np.uint8)
	grey_background_masked = cv2.bitwise_or(grey_background,mask_background)
	checkerboard_trans_cropped = cv2.bitwise_and(grey_background_masked,checkerboard_cropped)
	
	checkerboard_trans_file_name = "noised_checkerboard_weight_" + str(n_weight) + "_alpha_" + str(alpha_weight) + "_ref_" + str(color_trans) + "_cropped.png"
	
	
	# combine full and cropped images
	combined_image = np.concatenate((checkerboard_trans_cropped, checkerboard_trans), axis=1)
	# draw a frame
	cv2.rectangle(combined_image,(0,0),
					(2*n_image_size,n_image_size),
					(color_black,color_black,color_black),10)
	#cv2.imshow('circular_patch',combined_image)
	#cv2.waitKey()
	full_file_name = "combined_checkerboard_weight_" + str(n_weight) + "_alpha_" + str(alpha_weight) + "_ref_" + str(color_trans) + "_.png"
	cv2.cv2.imwrite(full_file_name,combined_image)
	
	
	cv2.imwrite(checkerboard_trans_file_name,checkerboard_trans_cropped)
	cv2.waitKey()
	return


# set parameters
f_file_name = "contrast_contrast_illusion_background.png"
c_file_name = "uncovered_checkerboard.png"
 
n_image_size = 600
color_background = 157

n_grid = 80
color_trans = 192 # reflectence of transparent medium [1,255]
n_weight = 0.0 # weight of noise [0,1]
alpha_weight = 0.2 # transparency of transparent mediumalpha [0,1]

# call functions
cci_background(n_grid,n_image_size,f_file_name) # create background noise
crop_checkerboard(color_trans,alpha_weight,crop_mask_name,n_image_size,color_background)

