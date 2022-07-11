#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 14:49:19 2019

Lasted Edited: 3/6/2020 to pull the y data from the tracking

@author: miles




The basic workflow of this notebook is to choose a video and generate the images.
Then, play with the cropping, color filters, and rotation in the "Single Frame Testing Ground"
Once the settings look good for a single frame, check how it looks on other frames.
Then, manually put the COM cuts and rotation angle in the AllCOM function and run!
"""

#Import
import numpy as np
from scipy import ndimage
import skimage.transform
from skimage import io
import matplotlib.pyplot as plt
import cv2
import glob
import os

"""""""""Functions"""""""""""
# Function to extract frames 
def FrameCapture(path,write):  
    # Path to video file 
    vidObj = cv2.VideoCapture(path) 
    
    # Used as counter variable, start at 1 because we already saved the first frame 
    count = 0
  
    # checks whether frames were extracted 
    success = 1
  
    while success: 
  
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read() 
        
        # Saves the frame
        if success == True:
            cv2.imwrite(write+'frames/frame%d.jpg' % count, image)
        
        count += 1

#Center of mass function
def COM(data):
    com = np.array(ndimage.measurements.center_of_mass(data)).astype(float)
    return com

#recombination of red, green, and blue channels
def Combine(red,green,blue):
    comb = np.zeros([len(red[:,0]),len(red[0,:]),3])
    comb[:,:,0]=red
    comb[:,:,1]=green
    comb[:,:,2]=blue
    comb=comb.astype(int)
    return comb

#seperate channels [3,y,x]
def Seperate(data):
    red = data[:,:,0]
    green = data[:,:,1]
    blue = data[:,:,2]
    return np.array([red,green,blue]).astype(int)
    
#get RGB averages/STD of a picture
def ColorAverage(data):
    red = np.average(data[:,:,0])
    green = np.average(data[:,:,1])
    blue = np.average(data[:,:,2])
    return np.array([red,green,blue]).astype(int)

def ColorSTD(data):
    redSTD = np.std(data[:,:,0])   
    greenSTD = np.std(data[:,:,1])
    blueSTD = np.std(data[:,:,2])
    
    colorstd = np.array([redSTD,greenSTD,blueSTD])
    
    return colorstd

def xSTD(data):
    std = np.std(data[:,1])
    
    return std

def ySTD(data):
    std = np.std(data[:,0])
    
    return std

def RedFilter(image):
    zeros=np.zeros([len(image[:]),len(image[0,:])])
    filtered=zeros
    
    #rgrat = np.divide(image[:,:,0],image[:,:,1])
    rbrat = np.divide(image[:,:,0],image[:,:,2])
    filtered[rbrat>1.8]=1
    filtered[rbrat<1.8]=0
    
    return filtered

def GreenFilter(image):
    zeros=np.zeros([len(image[:]),len(image[0,:])])
    filtered=zeros
    
    grrat = np.divide(image[:,:,1],image[:,:,0])
    gbrat = np.divide(image[:,:,1],image[:,:,2])
    filtered[grrat>2]=1
    filtered[gbrat<2]=0
    
    return filtered

def BlueFilter(image):
    zeros=np.zeros([len(image[:]),len(image[0,:])])
    filtered=zeros
    
    brrat = np.divide(image[:,:,2],image[:,:,0])
    #bgrat = np.divide(image[:,:,2],image[:,:,1])
    filtered[brrat>1.2]=1
    filtered[brrat<1.2]=0
    
    return filtered

def AllCOMs():
    """""""For loop for all frames"""""""""

    #MASSIVE FOR LOOP FOR EVERY FRAME LET'S GO BABY
    #data directories    
    for x in range(0,len(file_list)):
        img = io.imread(file_list[x])
        rotated = skimage.img_as_ubyte(skimage.transform.rotate(img,-2))
        crop = rotated[190:500,400:900,:]
        crop_back = crop/ColorAverage(crop)
        redfloat = RedFilter(crop_back)
        greenfloat = GreenFilter(crop_back)
        bluefloat = BlueFilter(crop_back)
        
        RGBCOM = np.array([COM(redfloat),COM(greenfloat),COM(bluefloat)])
        
        np.savetxt(data_dir+'COMs/'+'frame'+str(x)+'.out' ,RGBCOM)


"""data directory setup -- EDIT THE DATA_DIR FOR EACH DIFFERENT MOVIE"""

data_dir=('switch/cycle/')

if not os.path.exists(data_dir+'frames/'):
     os.makedirs(data_dir+'frames/')
if not os.path.exists(data_dir+'check/'):
     os.makedirs(data_dir+'check/')
if not os.path.exists(data_dir+'COMs/'):
     os.makedirs(data_dir+'COMs/')

"""Frame Generation"""
#Generate data from video
#This will take the chosen video and save jpg's of each and every frame. 
#Don't run this if you don't want thousands of pictures showing up in your data folder
"""CHANGE THE SAVE PATH"""
FrameCapture(data_dir+'switch_cycle_SAM_6932.MP4',data_dir)


"""Single Frame Testing Ground"""
#read data
file_list=sorted(glob.glob(data_dir+'frames/*.jpg'), key=os.path.getmtime)

#read single frame to get data type
img = io.imread(file_list[500])

#rotate to line up the axis of the device with the axis of the image
rotated = skimage.img_as_ubyte(skimage.transform.rotate(img,-2))

#crops to remove uneccesary information
crop = rotated[190:500,400:900,:]

#divides out the average background, make sure this makes sense
crop_back = crop/ColorAverage(crop)

#Run each through their filters
redfloat = RedFilter(crop_back)
greenfloat = GreenFilter(crop_back)
bluefloat = BlueFilter(crop_back)

np.savetxt('test.out',np.array([COM(redfloat),COM(greenfloat),COM(bluefloat)]))


"""generate all COMs"""
AllCOMs()

"""""""printouts:"""""""
print("Red: ","COM:", COM(redfloat))
print("Green: ","COM:", COM(greenfloat))
print("Blue: ", "COM:", COM(bluefloat))
print("background color:", ColorAverage(crop))

plt.imshow(crop)

f, axarr = plt.subplots(2,2)
axarr[0,0].imshow(crop_back)
axarr[0,1].imshow(redfloat)
axarr[1,0].imshow(greenfloat)
axarr[1,1].imshow(bluefloat)
