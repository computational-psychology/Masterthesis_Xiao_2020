# -*- coding: utf-8 -*-
"""
Some utility functions for creating checkerboard stimuli

@author: guille
"""

import numpy as np
import subprocess
import math
import string
import random



 # background color
light = 1.0  # light source 

letters = string.ascii_lowercase

def setcheckerboard(N, reflectances, samplerepeat):

    
    # constructing empty dictionary 
    r_checks = {}
    for i in range(N):
        for j in range(N):
            key = '%s%.2d' % (letters[i], j+1)
            r_checks[key] = None
       
    ##### setting 
    rest = N*N 
    
    v = np.repeat(reflectances, samplerepeat) # len(reflectances) repeated x times
    sample = list(np.random.choice(v, rest, replace=False))

    for key, value in r_checks.items():
        if value is None:
            r_checks[key] = sample.pop()
            
    return r_checks
    


def findsolution(N, reflectances, samplerepeat):
    """    
    Find a checkerboard arrangement of reflectances 
    
    """
    
    found = False
    redraw = True
    
    nn=0
    while not found:
        if redraw:
            
            #print("drawing entire checkerboard")
            r_checks = setcheckerboard(N, reflectances, samplerepeat)
        
        ret= checkcontiguous(r_checks)
        
        if ret[0]:
            found = True
            #print('%d checks were resampled' % nn)
        
        else:
            found = False
            
            #print("%s is being resampled" % ret[1])
            #if ret[1] in forbidden:
            #    print("but it's the forbidden list")
            #    redraw = True
            #else:
            #    redraw = False
            redraw=True
            #r_checks[ret[1]] = reflectances[random.randint(0, len(reflectances)-1)]
            nn+=1
            
    
    return r_checks



    
def getpositions(nC=10, xz1=-2.9, xz2=2.9, y1=-0.75, y2=-0.71):
    """
    Get xyz positions of a nC x nC checkerboard

    nC :        number of checks per side    
    xz1, xz2:   range in x and z coordinates of the checkerboard    
    y1, y2:     coordinates in the y dimension, i.e. the checkerboard height is y2-y1
    
    """
    
    coords = np.linspace(xz1, xz2, nC+1).round(2) 
        
    pos = {}
    for i in range(nC):
        for j in range(nC):
            key = '%s%.2d' % (letters[i], j+1)
            pos[key] = [[coords[i], y1, coords[j]], [coords[i+1], y2, coords[j+1]]]
            
    return pos



def checkcontiguous(r_checks, debug=False):
    """
    Check if contiguous check have same reflectance value
    Assumes a square checkerboard
    
    Returns a tuple, either (True, True) when there's no contigous reflectance 
    values in the entire checkerboard, or (False, label) where label is the 
    check label where the violation occurs and that needs to be replaced
    
    """
    nC = int(math.sqrt(len(r_checks)))
    
    for i in range(nC):
        for j in range(nC):
            n = j+1
            
            target = '%s%.2d' % (letters[i], n)
            
            if i<(nC-1):
                comp = '%s%.2d' % (letters[i+1], n)
                if r_checks[target]==r_checks[comp]:
                    if debug:
                        print("same reflectance in %s and %s" % (target, comp))
                    return (False, comp)
                
            if n<(nC):
                comp = '%s%.2d' % (letters[i], n+1)
                if r_checks[target]==r_checks[comp]:
                    if debug:
                        print("same reflectance in %s and %s" % (target, comp))
                    return (False, comp)
                             
    return (True, True)
    
    

def writetransparency(transparency, out_file):
    """
    Writes transparency specification into pov-ray file
    
    transparency: dictonary containing keys:    
        'xyz': list of 4 containing the xyz cooordinates of the transparency
        'transformation': string containing spatial transformation that can be applied to the transparency
        'color' and 'transmittance': transparency's reflectance  and transmittance
        
    """
    x1, y1, z1 = transparency['xyz'][0]
    x2, y2, z2 = transparency['xyz'][1]
    x3, y3, z3 = transparency['xyz'][2]
    x4, y4, z4 = transparency['xyz'][3]
    
    out_file.write('polygon{4, <%f, %f, %f> <%f, %f, %f> <%f, %f, %f> <%f, %f, %f>\n'
                    % (x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4))
                    
    if 'transformations' in transparency:
        out_file.write(transparency['transformations'])
    
    c1, c2, c3 = transparency['color']
    tr = transparency['transmit']
    
    out_file.write('texture{pigment {color rgb <%f, %f, %f> transmit %f}}}\n\n' % (c1, c2, c3, tr))
    
    
def write_pov(fname, r_checks, positions, transparency=None, cb_transf=None, planes=None, lightpos = 'right', pointers=None, background = 0.27):
    """
    Writes a Povray file .pov containing the specifications for rendering a variagated
    checkerboard with or without transparency.
    
    
    """
    ## write povray description file
    out_name = '%s.pov' % fname
    out_file = open(out_name, 'w')
    
    # povray version 3.7 needs specification of gamma. As it assumes 2.2, we need to give the same number 
    # so that the final gamma will be 1.0 (no gamma correction)
    
    #out_file.write('#version 3.7;\n\n')
    #out_file.write('global_settings {assumed_gamma 2.2}\n\n')
        
    
    out_file.write('background { color rgb <%2.2f, %2.2f,%2.2f>}\n\n' % tuple(np.repeat(background,3)))
    #out_file.write('#declare lens=camera{perspective location <0, 16,-50>  look_at <0,0,0>  angle 9.2};\n')
    out_file.write('#declare lens=camera{perspective location <0, 16,-50>  look_at <0,0,0>  angle 12};\n')
   
    out_file.write('camera{lens}\n\n')    

    if lightpos=='right':
        out_file.write('light_source{<20, 10, 7>  color rgb <%2.2f, %2.2f, %2.2f> area_light 6*x, 6*y, 12, 12}\n\n' % tuple(np.repeat(light,3)))
    elif lightpos=='left':
        out_file.write('light_source{<-20, 10, 7>  color rgb <%2.2f, %2.2f, %2.2f> area_light 6*x, 6*y, 12, 12}\n\n' % tuple(np.repeat(light,3)))

    
    
    # checkerboard   
    out_file.write('union{\n')
    for label, pos in positions.items():
        x1, y1, z1 = pos[0]
        x2, y2, z2 = pos[1]

        c1 = r_checks[label]
        c2 = c1
        c3 = c1
        
        out_file.write('box{<%f, %f, %f>, <%f, %f, %f> pigment{ color rgb <%f, %f, %f> }}// %s \n' % (x1, y1, z1, x2, y2, z2, c1, c2, c3, label))
    
    ### spatial  transformations for the checkerboard
    if cb_transf is not None:   
        out_file.write(cb_transf)
        
    out_file.write('}\n\n')

    ## planes 
    if planes is not None:
        for plane in planes:
            out_file.write(plane)
        
        
    ## writing transparencies
    if isinstance(transparency, dict):
        writetransparency(transparency, out_file)
        
    elif isinstance(transparency, tuple):
        for t in transparency:
            if t is not None:
                writetransparency(t, out_file)
    
       
    ## pointers indicating which checks to compare
    if pointers is not None:
        for line in pointers:
            out_file.write(line)
            
            
        
    # closes file
    out_file.close()
    
    return out_name



def runpovray(filename, res=(1024, 768)):
    """
    Calls povray for rendering file given as argument
    """
        
    return subprocess.call(["povray", "-W%d" % res[0], "-H%d" % res[1], "+A0.1", "Display=false", filename])


if __name__ == '__main__':
	
	### THIS MAIN PART RUNS AN EXAMPLE AND SHOWS HOW TO CALL THE FUNCTIONS ###
		
	# coordinates of the transparency
	# vertical, old one
	#COORDS = [[-1.4, 2.85, -8.0], [-1.4, 0.4, -8.0], [1.4, 0.4, -8.0], [1.4, 2.85, -8.0]]

	# horizontal, new one
	COORDS = [[-2.0, 1.85, -8.0], [-2.0, -0.2, -8.0], [2.0, -0.2, -8.0], [2.0, 1.85, -8.0]]


	def gettransparency(tau, alpha):
		
		transparency = {'xyz' :COORDS,
							'color': [tau, tau, tau], 
							'transmit': alpha,
							'transformations': 'rotate x *15\ntranslate<0, -2.3, 0>\n'}
		
		return transparency


	################### checkerboard specifications ##############################
	###########
	N = 7

	# choosing  reflectance values 
	# thirteen reflectance values as in Wiebel, Aguilar and Maertens 2017
	reflectances = np.array([0.06, 0.11, 0.19, 0.31, 0.46, 0.63, 0.82, 1.05, 1.29, 1.50, 1.67, 1.95, 2.22])

	# repeats from reflectance vector (#=13) where to draw non controlled checks (# = 10*10-9*3 = 73)
	samplerepeat = 9   

	## geometry of checkerboard
	pos = getpositions(nC=N, y1=-1.00, y2=-0.71)
	#  transformation
	cb_transf='rotate y * 45'



	### planes
	# added floor and walls
	planes=  None
	'''
	alphavec = np.arange(0, 0.51, 0.01)
	tau = 1.4
	aref = 0.05	
	rep = 3
	
	r_checks = findsolution(N, reflectances, samplerepeat)
	
	for alpha in alphavec:
	#######################  setting transparency STIM 
		alpha = round(alpha,2)
		transparency1 = gettransparency(tau, alpha)  # (tau, alpha)
		# tau goes from 1.0 to 7.0
		# alpha = 0 to 1
					
		#### write pov file   
		povfilename = 'rep_'+str(rep)+'_aref_'+str(aref)+"_tref_"+str(tau)+"_atest_"+str(alpha)
					
		write_pov(povfilename, r_checks=r_checks, positions=pos, cb_transf=cb_transf, 
								  planes=planes, transparency=transparency1)

		### runs povray
		runpovray('%s.pov' % povfilename, res=(600, 600))  
'''
	alphavec = np.arange(0, 0.51, 0.01)
	tau = 1.0
	#aref = 0.05	
	
	for rep in range(0,5):
		## call
		#### find a checkerboard 
		r_checks = findsolution(N, reflectances, samplerepeat)

		for alpha in alphavec:
			#######################  setting transparency STIM 
			alpha = round(alpha,2)
			transparency1 = gettransparency(tau, alpha)  # (tau, alpha)
			# tau goes from 1.0 to 7.0
			# alpha = 0 to 1
					
			#### write pov file   
			povfilename = 'rep_'+str(rep)+ "_tref_"+str(tau)+"_atest_"+str(alpha)
					
			write_pov(povfilename, r_checks=r_checks, positions=pos, cb_transf=cb_transf, 
								  planes=planes, transparency=transparency1)

			### runs povray
			runpovray('%s.pov' % povfilename, res=(600, 600))

   
	
# EOF
