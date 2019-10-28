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
import cv2

"""directories and data info"""
data_dir='/home/miles/Desktop/Python/data/float_tracker/ratchet/'
file_list=sorted(glob.glob(data_dir+'COMs/*.out'), key=os.path.getmtime)
img_file_list=sorted(glob.glob(data_dir+'frames/*.jpg'), key=os.path.getmtime)

frame_ratio = 10
camera_FPS=30
pixel_ratio=10.3  #pixels/mm
speed = 35/20 #mm/second

"""functions"""
def ReadCOM(frame_ratio):
    
    COM = np.zeros([3,2,int(len(file_list)/frame_ratio)])

    for x in range(0,int(len(file_list)/frame_ratio)):
        frame_data = np.loadtxt(file_list[x*frame_ratio])
        COM[:,:,x] = frame_data
    return COM
        
def CheckFrame(frame,channel):
    img = io.imread(img_file_list[frame])
    img = img[300:380,610:690,:] #use same cropping as you did in float_tracker.py!!!
    
    frame_data = np.loadtxt(file_list[frame])
    COM = frame_data
    
    plt.imshow(img)
    plt.scatter(COM[channel,1],COM[channel,0])
    
    plt.show()
    print(COM[channel])
 
def AngleCheck(frame,northpole,southpole):
    img = io.imread(img_file_list[frame])
    img = img[300:380,610:690,:] #use same cropping as you did in float_tracker.py!!!
    frame_data = np.loadtxt(file_list[frame])
    COM = frame_data
    
    plt.imshow(img)
    plt.arrow(COM[northpole,1],COM[northpole,0],COM[southpole,1]-COM[northpole,1],COM[southpole,0]-COM[northpole,0],color='yellow',linewidth=5,head_width=2)
    
    plt.show()

    
def GenerateAllFramesCOMCheck(FPS,frame_ratio):
    for x in range(0,int(len(file_list)/frame_ratio)):
        img = io.imread(img_file_list[x*frame_ratio])
        img = img[300:380,610:690,:] #use same cropping as you did in float_tracker.py!!!
        plt.imshow(img)
        
        frame_data = np.loadtxt(file_list[x*frame_ratio])
        COM = frame_data
        plt.scatter(COM[0,1],COM[0,0],color='r')
        plt.scatter(COM[1,1],COM[1,0],color='g')
        plt.scatter(COM[2,1],COM[2,0],color='b')
        
        plt.savefig(data_dir+'check/frame'+str(x)+'.png', dpi=500)
        plt.clf()
    
    img_array = []
    for filename in sorted(glob.glob(data_dir+'check/*.png'), key=os.path.getmtime):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        
    out = cv2.VideoWriter(data_dir+'VideoCheck.avi',cv2.VideoWriter_fourcc(*'DIVX'), FPS, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    
def GenerateAllFramesAngleCheck(FPS,frame_ratio,northpole,southpole):
    for x in range(0,int(len(file_list)/frame_ratio)):
        img = io.imread(img_file_list[x*frame_ratio])
        img = img[300:380,610:690,:] #use same cropping as you did in float_tracker.py!!!
        plt.imshow(img)
        
        frame_data = np.loadtxt(file_list[x*frame_ratio])
        COM = frame_data
        plt.arrow(COM[northpole,1],COM[northpole,0],COM[southpole,1]-COM[northpole,1],COM[southpole,0]-COM[northpole,0],color='yellow',linewidth=5,head_width=2)
    
        
        plt.savefig(data_dir+'check/frame'+str(x)+'.png', dpi=500)
        plt.clf()
        
    img_array = []
    for filename in sorted(glob.glob(data_dir+'check/*.png'), key=os.path.getmtime):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        
    out = cv2.VideoWriter(data_dir+'VideoCheck.avi',cv2.VideoWriter_fourcc(*'DIVX'), FPS, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
        
        
#def GenerateVideoCheck(FPS):
#
#    img_array = []
#    for filename in sorted(glob.glob(data_dir+'check/*.png'), key=os.path.getmtime):
#        img = cv2.imread(filename)
#        height, width, layers = img.shape
#        size = (width,height)
#        img_array.append(img)
#        
#    out = cv2.VideoWriter(data_dir+'VideoCheck.avi',cv2.VideoWriter_fourcc(*'DIVX'), FPS, size)
#     
#    for i in range(len(img_array)):
#        out.write(img_array[i])
#    out.release()
    
def Plot1(COM):
    plt.title('')
    plt.ylabel('Z-distance (mm)',fontsize = 24) 
    plt.xlabel('X-distance (mm)',fontsize = 24)
    plt.ylim(56*speed,0)
    plt.yticks(fontsize = 15)
    plt.xlim(0,45)
    plt.xticks(fontsize = 15)
    plt.scatter(-(COM[0,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS*speed,frame_ratio/camera_FPS*speed))-31*speed,color='r',marker='.')
    plt.scatter(-(COM[1,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS*speed,frame_ratio/camera_FPS*speed))-31*speed, color='g',marker='.')
    plt.scatter(-(COM[2,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS*speed,frame_ratio/camera_FPS*speed))-31*speed,color='b',marker='.')
#    plt.plot(COM[0,1,:].astype(int),(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS,frame_ratio/camera_FPS)),color='r')
#    plt.plot(COM[1,1,:].astype(int),(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS,frame_ratio/camera_FPS)), color='g')
#    plt.plot(COM[2,1,:].astype(int),(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS,frame_ratio/camera_FPS)),color='b')    
    

    fig = plt.gcf()
    fig.set_size_inches(5,10)
    plt.tight_layout()
    plt.savefig(data_dir+'paper_fig2D_2.png', dpi=300)
    plt.savefig('paper_fig2D_2.png', dpi=300)
    plt.show()
    
    
""""""""""""
#COM = ReadCOM(frame_ratio)
#GenerateAllFramesCOMCheck(5,frame_ratio)
GenerateAllFramesAngleCheck(5,frame_ratio,0,2)
#Plot1(COM)
#CheckFrame(0,0)
#print(COM[:,:,338])
#AngleCheck(0,0,2)