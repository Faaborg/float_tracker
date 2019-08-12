#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 14:49:19 2019

@author: miles
"""

#Import
import numpy as np
from scipy import ndimage
from skimage import io
import matplotlib.pyplot as plt
import cv2

"""""""""Functions"""""""""""
# Function to extract frames 
def FrameCapture(path): 
      
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
        cv2.imwrite("/home/miles/Desktop/Python/data/float_tracker/TaichiRGB/frame%d.jpg" % count, image)
        
        count += 1

#Center of mass function
def COM(data):
    com = ndimage.measurements.center_of_mass(data)
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

#filter using the full (cropped) image and the supercrop of a specific float
def Filter(image,supercrop):
    floatcoloraverage = ColorAverage(supercrop)
    floatcolorSTD = ColorSTD(supercrop)
    floatcolorSTD[floatcolorSTD<1]=1 #to keep everything from exploding when the average and std of a channel are 0, which actually happened
    
    zeros=np.zeros([len(image[:]),len(image[0,:])])
    filtered=zeros
    
#    redsignal = abs(image[:,:,0]-floatcoloraverage[0]) < floatcolorSTD[0]*redcutoff
#    greensignal = abs(image[:,:,1]-floatcoloraverage[1]) < floatcolorSTD[1]*greencutoff
#    bluesignal = abs(image[:,:,2]-floatcoloraverage[2]) < floatcolorSTD[2]*bluecutoff
    redsignal = abs(image[:,:,0]-floatcoloraverage[0]) < redcutoff
    greensignal = abs(image[:,:,1]-floatcoloraverage[1]) < greencutoff
    bluesignal = abs(image[:,:,2]-floatcoloraverage[2]) < bluecutoff
    fullmatch = np.logical_and(redsignal,greensignal,bluesignal)
    
    filtered[fullmatch]=1
    return filtered



"""The following will need to be tweaked manually for each analysis. 
It is crucial that for each video, you do the supercrop around each float to establish the float colors"""
#read data
img = io.imread('/home/miles/Desktop/Python/data/float_tracker/TaichiRGB/frame2192.jpg')

#This will take the chosen video and save jpg's of each and every frame. 
#Don't run this if you don't want thousands of pictures showing up in your data folder
#out = FrameCapture('/home/miles/Desktop/Python/data/float_tracker/TaichiRGB/400 mm p min.MP4')


#crops to remove uneccesary information
crop = img[300:400,250:1200,:]

#divides out the average background
crop_back = crop/ColorAverage(crop)

#get colors of each float FROM A SINGLE REPRESENTATIVE IMAGE: frame2192
supercrop_redfloat = crop_back[40:80,850:890,:]
supercrop_greenfloat = crop_back[38:78,80:120,:]
supercrop_bluefloat = crop_back[35:75,132:172,:]

#set filter thresholds, each value is the number of 
#standard deviations from the mean value of each channel of the supercrop of each float
redcutoff = 0.5
greencutoff = 0.5
bluecutoff = 0.1


"""""""business end"""""""""

redfloat = Filter(crop_back,supercrop_redfloat)
greenfloat = Filter(crop_back,supercrop_greenfloat)
bluefloat = Filter(crop_back,supercrop_bluefloat)

"""""""printouts:"""""""

print("redCOM: ", COM(redfloat), ColorAverage(supercrop_redfloat), ColorSTD(supercrop_redfloat))
print("greenCOM: ", COM(greenfloat), ColorAverage(supercrop_greenfloat))
print("blueCOM: ", COM(bluefloat), ColorAverage(supercrop_bluefloat))

f, axarr = plt.subplots(2,2)
axarr[0,0].imshow(crop_back)
axarr[0,1].imshow(redfloat)
axarr[1,0].imshow(greenfloat)
axarr[1,1].imshow(bluefloat)





#print("red", np.average(supercrop_redfloat[:,:,0]))
#print("green", np.average(supercrop_redfloat[:,:,1]))
#print("blue", np.average(supercrop_redfloat[:,:,2]))
#
#print("red", np.average(supercrop_yellowfloat[:,:,0]))
#print("green", np.average(supercrop_yellowfloat[:,:,1]))
#print("blue", np.average(supercrop_yellowfloat[:,:,2]))
#
#print("red", np.average(supercrop_bluefloat[:,:,0]))
#print("green", np.average(supercrop_bluefloat[:,:,1]))
#print("blue", np.average(supercrop_bluefloat[:,:,2]))