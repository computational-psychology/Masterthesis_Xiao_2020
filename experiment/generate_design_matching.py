# -*- coding: utf-8 -*-
import numpy as np
import itertools
import random
import pandas as pd


"""
Design Matrix
1 Trial range(0,12)
2 Repeat range(0,10)
4 Position 0/1

"""

# values
nTrial = 12
nRepeat = 10

obsname = 'sub5' 

def trp_shuffle():
    t = []
    t1 = np.repeat(range(0,nTrial), nRepeat)
    r1 = np.tile(range(0,nRepeat),nTrial)
#    r1 = np.tile(4,nTrial)
    p1 = np.repeat([0,1],nTrial*nRepeat/2)
    trp = np.row_stack((t1,r1,p1))
    ind = list(range(0, nTrial*nRepeat))
    random.shuffle(ind)
    for i in range(0, nTrial*nRepeat):
        t2 = trp[:,ind[i]]
        t = np.append(t,t2)
    t = np.reshape(t, (nTrial*nRepeat,3))
	#t = np.transpose(t)
    return t
	
t1 = trp_shuffle()
#t2 = trp_shuffle()
#t3 = trp_shuffle()
#t4 = trp_shuffle()
#t5 = trp_shuffle()

#m = np.row_stack((t1,t2,t3,t4,t5))

# creates dataframe with all trials
des = pd.DataFrame(t1, columns=["Trial", "Rep", "Pos"])
#des = pd.DataFrame(m, columns=["Trial", "Rep", "Pos"])
		
des.index.name = 'N'
		
# save in design folder, under block number

des.to_csv("design_matching/%s/%s.csv" % (obsname, obsname))

