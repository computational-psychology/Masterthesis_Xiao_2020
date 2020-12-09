# -*- coding: utf-8 -*-
"""
This is a script for generating the contrast contrast illusion from
Chubb, Sperling & Solomon, 1989

@author: Dogson
"""

import numpy as np
import cv2
import random


color_grey = 127

def cci_background(n_grid,n_image_size,f_file_name):
	# n_grid: number of rectangles to be created
	# n_image_size: size of the background image in pixel
	# n_grid must be a sivisor of n_image_size
	# f_file_name: name of the file to be created
	color_white = 255
	color_black = 0

	
	# create a black background
	img = np.zeros((n_image_size,n_image_size,3), np.uint8)
	
	# prepare colors that would be later fill into rectangles
	colors = np.array([color_black,color_white])
		
	
	# draw black or white rectangles on the black background
	for i in range(n_grid):
		for j in range(n_grid):
			k = i+1
			l = j+1
			random.shuffle(colors)
			color = int(colors[0])
			cv2.rectangle(img,(i*n_image_size//n_grid,j*n_image_size//n_grid),
					(k*n_image_size//n_grid,l*n_image_size//n_grid),
					(color,color,color),-1)
	
	# draw a half rectangle
	cv2.rectangle(img,(0,int(1/2*n_image_size)),
					(n_image_size,n_image_size),
					(color_grey,color_grey,color_grey),-1)
	#cv2.imshow('contrast contrast illusion - background',img)
	#cv2.waitKey()
	# write the image
	cv2.imwrite(f_file_name,img)
	return




# function for adding a circular patch
def add_circular_patch(f_file_name, n_circle_radius,n_circle_color,n_weight,n_file_name):
	# f_file_name: file name of the background image
	# n_circle_radius: radius of the circular patch
	# n_circle_color: color of the central patch
	# n_weight：transparency of the circular patch [0,1]
	# n_file_name: name of the file to be created
	
	# import the background image
	background_noise = cv2.imread(f_file_name)
	background_add_circle = cv2.imread(f_file_name)
	
	# draw a mid grey circle over the background
	cv2.circle(background_add_circle,(n_circle_center,n_circle_center), 
									   n_circle_radius, 
									   (n_circle_color,n_circle_color,n_circle_color), -1)
	#cv2.imshow('background',background_noise)
	#cv2.imshow('background + circle',background_add_circle)
	#cv2.waitKey()
	
	# add background and the circle with a certain weight
	target_image = cv2.addWeighted(background_add_circle,1-n_weight,background_noise,
								   n_weight,0)
	#cv2.imshow('background + circle',target_image)
	#cv2.waitKey()
	# write the image
	cv2.imwrite(n_file_name,target_image)
	return






def crop_circular_patch(n_image_size,n_circle_center,n_circle_radius,
						n_file_name,s_file_name):
	# import the background image
	background_high_contrast = cv2.imread(n_file_name)
	#cv2.imshow('background + circle',background_high_contrast)
	#cv2.waitKey()
	
	# create a mask with a white background and a black cirle
	color_white = 255
	color_black = 0
	mask = np.full((n_image_size, n_image_size, 3), color_white, np.uint8) 
	mask = cv2.circle(mask,(n_circle_center,n_circle_center),n_circle_radius, 
					  (color_black,color_black,color_black), -1)
	#cv2.imshow('mask',mask)
	#cv2.waitKey()
	
	# crop the the circular patch
	circular_patch = cv2.bitwise_or(background_high_contrast,mask)
	#cv2.imshow('circular_patch',circular_patch)
	#cv2.waitKey()
	
	# place the circular patch on a grey backgroud
	# create a grey background
	grey_background = np.full((n_image_size, n_image_size, 3), color_grey, np.uint8)
	cv2.circle(grey_background,(n_circle_center,n_circle_center),n_circle_radius, 
					  (color_white,color_white,color_white), -1) 
	background_low_contrast = cv2.bitwise_and(grey_background,circular_patch)
	#cv2.imshow('circular_patch',background_low_contrast)
	#cv2.waitKey()
	cv2.imwrite(s_file_name,background_low_contrast)
	# combine high and low contrast background images
	combined_image = np.concatenate((background_low_contrast, background_high_contrast), axis=1)
	# draw a frame
	cv2.rectangle(combined_image,(0,0),
					(2*n_image_size,n_image_size),
					(color_black,color_black,color_black),10)
	#cv2.imshow('circular_patch',combined_image)
	#cv2.waitKey()
	cv2.cv2.imwrite(full_file_name,combined_image)
	return



################


# call function function
def call_function(n_grid,n_image_size,f_file_name,n_file_name,s_file_name,
				  n_circle_center,n_circle_radius,n_circle_color):
	cci_background(n_grid,n_image_size,f_file_name)
	add_circular_patch(f_file_name, n_circle_radius,n_circle_color,n_weight,n_file_name)
	crop_circular_patch(n_image_size,n_circle_center,n_circle_radius,
						n_file_name,s_file_name)
	return


# call functions

# set parameters
n_grid = 80 # number of noise grids per line
n_image_size = 600
n_weight = 0.1 # transparency alpha
n_circle_color = 120 # reflectence tau
f_file_name = "half_contrast_contrast_illusion_background_"+str(n_image_size)+".png"
n_file_name = "half_contrast_contrast_illusion_high_contrast_background_"+str(n_image_size)+"_alpha_"+str(n_weight)+"_ref_"+str(n_circle_color)+".png"
s_file_name = "half_contrast_contrast_illusion_low_contrast_background_"+str(n_image_size)+"_alpha_"+str(n_weight)+"_ref_"+str(n_circle_color)+".png"
full_file_name = "half_contrast_contrast_illusion_"+str(n_image_size)+"_alpha_"+str(n_weight)+"_ref_"+str(n_circle_color)+".png"
n_circle_center = int(1/2*n_image_size)
n_circle_radius = int(1/8*n_image_size) #measured approximately from the original illusion


# call call function function
call_function(n_grid,n_image_size,f_file_name,n_file_name,s_file_name,
			  n_circle_center,n_circle_radius,n_circle_color)
