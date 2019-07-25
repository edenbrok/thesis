# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 15:06:45 2019

@author: Emma
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pandas as pd

def region_extraction(chosen_region, decision_type):
    l = []
    #the EMA results are a string, but if you save them in a pandas csv tey become floats
    #so cast them back into a string again!
    

    if math.isnan(chosen_region):
        return l
    else:
        chosen_region = str(int(chosen_region))
        if decision_type == 0:
            l.append(int(chosen_region))
            return l
        else:
            length = len(chosen_region)
            n = int(length / 2) #the length of the string divided by 2 is the no of regions chosen
            for i in range (0,n):
                r = chosen_region[2*i:2*i+2]
                l.append(int(r)-10)
            return l



def array_coord(region_no, grid_size):
    row = math.sqrt(grid_size)
    i = int(region_no/row)
    j = int(region_no % row)
    
    return i, j

#from model import ebola_model

outcomes = pd.read_csv('result_test.csv')

results = pd.read_csv('save_test.csv')

regions = [[0,1,2,3],
           [4,5,6,7],
           [8,9,10,11],
           [12,13,14,15]]

# Now we can do the plotting!
fig, ax = plt.subplots(1, figsize=(1, 1))
# Remove a bunch of stuff to make sure we only 'see' the actual imshow
# Stretch to fit the whole plane
#fig.subplots_adjust(0, 0, 1, 1)
# Remove bounding line

#ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
#ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)


plt.xticks([-0.5, 0.5, 1.5, 2.5, 3.5 ])
plt.yticks([-0.5, 0.5, 1.5, 2.5, 3.5 ])

ax.grid(color="w", linestyle='-', linewidth=2)
#ax.axis("off")

## Remove ticks and labels
for axi in (ax.xaxis, ax.yaxis):
    for tic in axi.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False

text = regions
for i in range(4):
    for j in range(4):
        text[i][j] = ax.text(j, i, regions[i][j],
                       ha="center", va="center", color="w", fontsize="small") 

## DECISIONS OVER TIME ##

a=np.full((4,4),0.5)
im = plt.imshow(a, cmap='Spectral', vmin=0, vmax=1)

ax.set_title("Decision Types Over Time", fontsize=5, pad=2)


# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame


ims = []


for i in range(27):
    if i < 26:
        #make a list of all the regions affected by decisions in timestep i
        l = region_extraction(outcomes['Chosen Regions'][i], outcomes['Decision Types'][i])
        for r in l:
            k,j = array_coord(r, 16)
            if outcomes['Decision Types'][i] == 0:
                if a[k][j] > 0.5:
                    a[k][j] = 0.5
                a[k][j] -= 0.1
            else:
                if a[k][j] < 0.5:
                    a[k][j] = 0.5
                a[k][j] += 0.1
     
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
   
            
    im = ax.imshow(a, cmap='Spectral', vmin=0, vmax=1)
    


    
    #add_arts = [im, ]
    
    ims.append([im])






ani_decisions = animation.ArtistAnimation(fig, ims, interval=1000, blit=True)

ani_decisions.save('decisions.mp4', dpi=512)




## UNCERTAINTY ##

b =np.ones((4,4))

im2 = plt.imshow(b, cmap='binary', vmin=0, vmax=1)

ax.set_title("Uncertainty Over Time", fontsize=5, pad=2)

ims2 = [[im2]]


#for each timestep
for i in range(27):
    #for each region update the array
    for j in range(16):
        m,n = array_coord(j, 16)
        b[m][n] = (results['Uncertainty'][i+(j*27)])/3
            
    im2 = plt.imshow(b, cmap='binary', vmin=0, vmax=1)
    ims2.append([im2])

ani_uncertainty = animation.ArtistAnimation(fig, ims2, interval=1000, blit=False)

ani_uncertainty.save('uncertainty.mp4', dpi=512)

## ACTUAL CASES ##

c = np.zeros((4,4,))

im3 = plt.imshow(c, cmap='Reds', vmin=0, vmax=1)

ax.set_title("Actual Cases", fontsize=5, pad=2)

ims3 = [[im3]]

max_cases = results['I'].max()
for i in range(27):
    for j in range(16):
        m,n = array_coord(j,16)
        c[m][n] = (results['I'][i+(j*27)])/3
        
    im3 = plt.imshow(c, cmap='Reds', vmin=0, vmax=1)
    ims3.append([im3])
    
ani_cases = animation.ArtistAnimation(fig, ims3, interval=1000, blit=False)

ani_cases.save('cases.mp4', dpi=512)


## OBSERVED CASES (MIN) ##

d = np.zeros((4,4,))

im4 = plt.imshow(d, cmap='Reds', vmin=0, vmax=1)

ax.set_title("Observed Cases", fontsize=5, pad=2)

ims4 = [[im4]]

max_cases = results['I'].max()
for i in range(27):
    for j in range(16):
        m,n = array_coord(j,16)
        d[m][n] = (results['Observed I'][i+(j*27)])/3
        
    im4 = plt.imshow(d, cmap='Reds', vmin=0, vmax=1)
    ims4.append([im4])




   
# plt.colorbar(im4)

ani_obs_cases = animation.ArtistAnimation(fig, ims4, interval=1000, blit=False)

ani_obs_cases.save('observed_cases.mp4', dpi=512)