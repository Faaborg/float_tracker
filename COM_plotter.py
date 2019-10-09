#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 11:33:17 2019

@author: miles
"""

import numpy as np
import glob
import os
from skimage import io
import matplotlib.pyplot as plt

"""directories and data info"""
data_dir=('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_COMs/')
file_list=sorted(glob.glob(data_dir+'*.out'), key=os.path.getmtime)
img_data_dir=('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_frames/')
img_file_list=sorted(glob.glob(img_data_dir+'*.jpg'), key=os.path.getmtime)

frame_ratio = 30
camera_FPS=30

"""functions"""
def ReadCOM(frame_ratio):
    
    COM = np.zeros([3,2,len(file_list)/frame_ratio])

    for x in range(0,int(len(file_list)/frame_ratio)):
        frame_data = np.loadtxt(file_list[x*frame_ratio])
        COM[:,:,x] = frame_data
    return COM
        
def CheckFrame(frame,channel):
    img = io.imread(img_file_list[frame])
    img = img[320:390,400:900,:] #use same cropping as you did in float_tracker.py!!!
    
    frame_data = np.loadtxt(file_list[frame])
    COM = frame_data
    
    plt.imshow(img)
    plt.scatter(COM[channel,1],COM[channel,0])
    
    plt.show()
    print(COM[channel])
    
def GenerateVideoCheck(frame_ratio):
    for x in range(0,int(len(file_list)/frame_ratio)):
        img = io.imread(img_file_list[x*frame_ratio])
        img = img[320:390,400:900,:] #use same cropping as you did in float_tracker.py!!!
        plt.imshow(img)
        
        frame_data = np.loadtxt(file_list[x*frame_ratio])
        COM = frame_data
        plt.scatter(COM[0,1],COM[0,0],color='r')
        plt.scatter(COM[1,1],COM[1,0],color='g')
        plt.scatter(COM[2,1],COM[2,0],color='b')
        
        plt.savefig('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_check/frame'+str(x)+'.png', dpi=500)
        plt.clf()


    
"""business"""
GenerateVideoCheck(frame_ratio)
"""Final Plots"""
#plt.title('X-position of floats versus time')
#plt.ylabel('Time (seconds)')
#plt.ylim(TIME+10,-10)
#plt.xlabel('X-position (pixels)')
#plt.plot(COM[0,1,:].astype(int),np.flip(np.arange(0,TIME,frame_ratio/camera_FPS)),color='r')
#plt.plot(COM[1,1,:].astype(int),np.flip(np.arange(0,TIME,frame_ratio/camera_FPS)), color='g')
#plt.plot(COM[2,1,:].astype(int),np.flip(np.arange(0,TIME,frame_ratio/camera_FPS)),color='b')
#
#plt.show()