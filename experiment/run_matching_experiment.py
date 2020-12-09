#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Matching experiment

Script recycled from Christiane's script

@author: experimenter
"""

### Imports ###
# Package Imports
from hrl import HRL
from hrl.graphics import graphics
import pygame as pg
import OpenGL.GL as gl

# Qualified Imports
import numpy as np
from PIL import Image
import random
import sys
import os
import Image, ImageFont, ImageDraw

# size of monitor
WIDTH=1024
HEIGHT=768


# compute center of the screen
whlf = WIDTH/2.0
hhlf = HEIGHT/2.0
    
    
## Functions which are needed for the experiment   
def warning_min(hrl):
    # function that generates a beep tone
    #status=  os.system('beep')
    # print "beep status ", + status
    hrl.graphics.flip(clr=True)
    lines = [u'Minimum erreicht!',
             u' ',
             u'Zum Weitermachen, drücke die mittlere Taste.']
    for line_nr, line in enumerate(lines):
        textline = hrl.graphics.newTexture(draw_text(line, fontsize=36))
        textline.draw(((1024 - textline.wdth) / 2,
                       (768 / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
    
def warning_max(hrl):
    # function that generates a beep tone
    #status=  os.system('beep')
    # print "beep status ", + status
    hrl.graphics.flip(clr=True)
    lines = [u'Maximum erreicht!',
             u' ',
             u'Zum Weitermachen, drücke die mittlere Taste.']
    for line_nr, line in enumerate(lines):
        textline = hrl.graphics.newTexture(draw_text(line, fontsize=36))
        textline.draw(((1024 - textline.wdth) / 2,
                       (768 / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
    
      
def show_stimulus(hrl, reference, textures, match_alpha, ref_side):
    """
    Show reference stimulus and match stimulus side by side
    textures is a list of all possible adjustments in the test side
    
    match_alpha is the index for that list
    
    """
    
    if ref_side==0:
        refpos = (0, hhlf - reference.hght/2)
        testpos = (whlf, hhlf - textures[match_alpha].hght/2)
        
    elif ref_side==1:
        refpos = (whlf - 10, hhlf - reference.hght/2)
        testpos = (0, hhlf - textures[match_alpha].hght/2)
        
    else:
        raise("Error on reference side coding")

    # draws reference
    reference.draw(refpos)
    
    # draws test
    textures[match_alpha].draw(testpos)
    
    hrl.graphics.flip(clr=False)   # clr= True to clear buffer
    
        
def read_design(fname):
    # function written by Marianne
    
    design = open(fname)
    header = design.readline().strip('\n').split()
    data   = design.readlines()
    
    new_data = {}
    
    for k in header:
        new_data[k] = []
    for l in data:
        curr_line = l.strip().split()
        for j, k in enumerate(header):
            new_data[k].append(curr_line[j])
    return new_data


def read_design_csv(fname):
    
    
    design = open(fname)
    header = design.readline().strip('\n').split(',')
    #print header
    data   = design.readlines()
    
    new_data = {}
    
    for k in header:
        new_data[k] = []
    for l in data:
        curr_line = l.strip().split(',')
        for j, k in enumerate(header):
            new_data[k].append(curr_line[j])
    return new_data
    

def adjust_loop(hrl, reference, textures, match_alpha, ref_side):
    
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
        
        if btn == 'Up':
            match_alpha = int(match_alpha + bgs)
            if  match_alpha > maxalphaindx:
                 warning_max(hrl)
                 match_alpha = maxalphaindx
            elif match_alpha  < minalphaindx :
                 warning_min(hrl)
                 match_alpha  = minalphaindx 
                 
            print 'match alpha idx', match_alpha
            show_stimulus(hrl, reference, textures, match_alpha, ref_side)
            
        elif btn == 'Down':
            match_alpha = int(match_alpha - bgs)
            if  match_alpha > maxalphaindx:
                 warning_max(hrl)
                 match_alpha = maxalphaindx
            elif match_alpha  < minalphaindx :
                 warning_min(hrl)
                 match_alpha  = minalphaindx 
                 
            print 'match alpha idx', match_alpha
            show_stimulus(hrl, reference, textures, match_alpha, ref_side)
            
        elif btn == 'Right':
            match_alpha = int(match_alpha + sms)
            if  match_alpha > maxalphaindx:
                 warning_max(hrl)
                 match_alpha = maxalphaindx
            elif match_alpha  < minalphaindx :
                 warning_min(hrl)
                 match_alpha  = minalphaindx 
                 
            print 'match alpha idx', match_alpha
            show_stimulus(hrl, reference, textures, match_alpha, ref_side)
            
        elif btn == 'Left':
            match_alpha = int(match_alpha - sms)
            if  match_alpha > maxalphaindx:
                 warning_max(hrl)
                 match_alpha = maxalphaindx
            elif match_alpha  < minalphaindx :
                 warning_min(hrl)
                 match_alpha  = minalphaindx 

            print 'match alpha idx', match_alpha
            show_stimulus(hrl, reference, textures, match_alpha, ref_side)
            
        elif btn == 'Space':
            print 'space'
            
        if hrl.inputs.checkEscape():
        
            print 'Abort! Abort!'
            hrl.close()
            sys.exit(0)
    
    #print "MatchLum =", match_lum
    #print "Button = ", btn
    return match_alpha, btn

def show_match(hrl, match_lum, curr_match):
    # replace the center patch on top of the match_display  and adjust it to the matched lumiances:
    center = np.copy(curr_match)
    center[center== 1.0] = match_lum
    # create new texture
    center_display = hrl.graphics.newTexture(center)
    return(center_display)


def get_last_trial(vp_id):
    try:
        rfl =open('results_matching/%s/%s.txt' %(vp_id, vp_id), 'r')
    except IOError:
        print 'result file not found'
        return 0
        
    for line in rfl:
        try:
            last_trl = int(line.split('\t')[0])
        except ValueError:
            pass
    
    if last_trl>0:
        last_trl=last_trl+1
        
    return last_trl
    
def draw_text(text, bg=0.27, text_color=0, fontsize=48):
    # function from Torsten
    """ create a numpy array containing the string text as an image. """

    bg *= 255
    text_color *= 255
    font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/arial.ttf", fontsize,
            encoding='unic')
    text_width, text_height = font.getsize(text)
    im = Image.new('L', (text_width, text_height), bg)
    draw = ImageDraw.Draw(im)
    draw.text((0,0), text, fill=text_color, font=font)
    return np.array(im) / 255.


def show_break(hrl,trial, total_trials):
    # Function from Torsten
    hrl.graphics.flip(clr=True)
    lines = [u'Du kannst jetzt eine Pause machen.',
             u' ',
             u'Du hast %d von %d Durchgängen geschafft.' % (trial,
                 total_trials),
             u' ',
             u'Wenn du bereit bist, drücke die mittlere Taste.'
             ]
    for line_nr, line in enumerate(lines):
        textline = hrl.graphics.newTexture(draw_text(line, fontsize=36))
        textline.draw(((1024 - textline.wdth) / 2,
                       (768 / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()


def run_trial(hrl,trl, start_trl, end_trl):
    # function written by Torsten and edited by Christiane
    # read out variable values for each trial from the designmatrix
    print "TRIAL =", trl
    
    print trl
    print start_trl
    print end_trl
    #show break automatically, define after how many trials
    if (trl-start_trl)%50==0:
        show_break(hrl,(trl-start_trl), (end_trl-start_trl))
    
    # get values from design matrix for current trial
    trl_id = float(design['Trial'][trl])
    ref_side = float(design['Pos'][trl])
    rep_id = int(float(design['Rep'][trl]))
    
    if trl_id ==0 :
        t_ref = 2
        a_test = 0.05
        rep = 0
    
    if trl_id ==1 :
        t_ref = 4
        a_test = 0.05
        rep = 0
        
    if trl_id == 2:
        t_ref = 6
        a_test = 0.05
        rep = 0
        
    if trl_id == 3:
        t_ref = 2
        a_test = 0.10
        rep = 1
    
    if trl_id == 4:
        t_ref = 4.0
        a_test = 0.10
        rep = 1
            
    if trl_id == 5:
        t_ref = 6
        a_test = 0.10
        rep = 1
    
    if trl_id == 6:
        t_ref = 2
        a_test = 0.20
        rep = 2
        
    if trl_id == 7:
        t_ref = 4
        a_test = 0.20
        rep = 2
        
    if trl_id == 8:
        t_ref = 6
        a_test = 0.20
        rep = 2
    
    if trl_id == 9:
        t_ref = 2
        a_test = 0.40
        rep = 3
        
    if trl_id == 10:
        t_ref = 4
        a_test = 0.40
        rep = 3
    
    if trl_id == 11:
        t_ref = 6
        a_test = 0.40
        rep = 3

    print trl_id
    print rep_id
    print rep
    print t_ref
    print a_test
      
        

    #a_ref = float(design['a_ref'][trl])
    #t_ref = float(design['t_ref'][trl])
    #t_test = float(design['t_test'][trl])
 
    
               
    # use these variable values to define test stimulus (name corresponds to design matrix and name of saved image)
    #trialname = 'rep_%d_aref_%.2f_tref_%.1f_atest_%.2f' % (rep, a_ref, t_ref, t_test)
    
    # reference file 
    stim_name = 'stimuli_matching/stimuli/rep_%d_tref_%d_atest_%.2f.png' % (rep, t_ref, a_test)
    #'%s/%s_ref_cropped.png' % (trialname)
    
    
    # texture creation in buffer : referece stimulus
    #reference = hrl.graphics.newTexture(curr_image)
    image = Image.open(stim_name).convert("L").resize((576, 576))
    im = np.asarray(image)/ 255.    
        
    # texture creation in buffer
    reference = hrl.graphics.newTexture(im)
    
    ### loading adjustment files
    textures = []
    for alpha in alpha_vec:
        teststimname =  'rep_%d_tref_%d_atest_%.2f' % (rep, t_ref, alpha)
        fname = 'stimuli_matching/stimuli/%s_cropped.png' % (teststimname)

        
        #print "loading... %s " % fname
        image = Image.open(fname).convert("L").resize((576, 576))
        im = np.asarray(image)/ 255.    
        
        # texture creation in buffer
        tex = hrl.graphics.newTexture(im)
        textures.append(tex)
        
    
    
    # random assignment of start match intensity between 0 and 1
    start_idx = random.randint(0, len(textures)-1)
    no_match       = True 
    match_alpha    = start_idx
    

    while no_match: # as long as no_match TRUE
    
        # Show stimuli: reference and test
        show_stimulus(hrl, reference, textures, match_alpha, ref_side)   
             
        match_alpha, btn = adjust_loop(hrl, reference, textures, match_alpha, ref_side)
        
        print "btn =", btn  
        print "match alpha index", match_alpha
        print "match alpha", alpha_vec[match_alpha]
        if btn == 'Space':
               no_match = False
    
    
    rfl.write('%d\t%d\t%f\t%f\t%d\t%d\t%d\t%d\t%f\n' % (trl, ref_side, a_test, t_ref, rep, rep_id, start_idx, match_alpha, alpha_vec[match_alpha]))
    rfl.flush()

    hrl.graphics.flip(clr=True)  
    
    # clean checkerboard texture 
       
    graphics.deleteTextureDL(reference._dlid)
    graphics.deleteTexture(reference._txid)
    
    for tex in textures:
        graphics.deleteTextureDL(tex._dlid)
        graphics.deleteTexture(tex._txid)
    
    
     
    return match_alpha
    



"""
main part of the code: here the experiment gets executed
"""


## 
vp_id   = raw_input ('Bitte geben Sie Ihre Initialen ein (z.B. mm): ')
start_trl = get_last_trial(vp_id)



sms = 1
bgs = 5

#if vp_id=='sub1' or vp_id=='sub2':
#    alpha_vec = np.arange(0.05, 0.46, 0.01)
#else:
alpha_vec = np.arange(0, 0.81, 0.01)


maxalphaindx = len(alpha_vec)-1
minalphaindx = 0


# read design file and open result file for saving 
design = read_design_csv('design_matching/%s/%s.csv' %(vp_id, vp_id))
rfl    = open('results_matching/%s/%s.txt' %(vp_id, vp_id), 'a')

# Pass this to HRL if we want to use gamma correction.
lut = 'lut.csv'   


end_trl = len(design['Trial'])

# file to save surround of match check
#fid_all_match = open('results/%s/%s_all_match_surr.txt' %(vp_id, vp_id), 'a')

if start_trl == 0:
    
    result_headers = ['trl','ref_side', 'a_test', 't_test', 'rep', 'rep_id', 'start_idx', 'matched_alpha_idx', 'matched_alpha']
    rfl.write('\t'.join(result_headers)+'\n')


def main():
     
    hrl = HRL(graphics='datapixx',
              inputs='responsepixx',
              photometer=None,
              wdth=WIDTH,
              hght=HEIGHT,
              bg=0.27,
              scrn=1,
              lut='lut.csv',
              db = False,
              fs=True)
   
    
    # loop over design
    # ================
    for trl in np.arange(start_trl, end_trl):
        run_trial(hrl, trl, start_trl, end_trl) # function that executes the experiment
        
        
    hrl.close()
    print "Session complete"
    rfl.close()

### Run Main ###
if __name__ == '__main__':
    main()
    




