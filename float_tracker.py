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
import glob
import os

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
        cv2.imwrite("/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_frames/frame%d.jpg" % count, image)
        
        count += 1

#Center of mass function
def COM(data):
    com = np.array(ndimage.measurements.center_of_mass(data))
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

def RedFilter(image):
    zeros=np.zeros([len(image[:]),len(image[0,:])])
    filtered=zeros
    
    rgrat = image[:,:,0]/image[:,:,1]
    rbrat = image[:,:,0]/image[:,:,2]
    filtered[rgrat>1.5]=1
    filtered[rbrat<1.5]=0
    
    return filtered

def GreenFilter(image):
    zeros=np.zeros([len(image[:]),len(image[0,:])])
    filtered=zeros
    
    grrat = image[:,:,1]/image[:,:,0]
    gbrat = image[:,:,1]/image[:,:,2]
    filtered[grrat>1.5]=1
    filtered[gbrat<1.5]=0
    
    return filtered

def BlueFilter(image):
    zeros=np.zeros([len(image[:]),len(image[0,:])])
    filtered=zeros
    
    brrat = image[:,:,2]/image[:,:,0]
    bgrat = image[:,:,2]/image[:,:,1]
    filtered[brrat>1.3]=1
    filtered[bgrat<1.3]=0
    
    return filtered


"""Frame Generation"""
#Generate data from video
#This will take the chosen video and save jpg's of each and every frame. 
#Don't run this if you don't want thousands of pictures showing up in your data folder
"""CHANGE THE SAVE PATH IN FRAMECAPTURE YOU GOOBER"""
#out = FrameCapture('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/SAM_6812.MP4')


"""Single Frame Testing Ground"""
#read data
data_dir=('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_frames/')
file_list=sorted(glob.glob(data_dir+'*.jpg'), key=os.path.getmtime)

#read single frame to get data type
img = io.imread(file_list[0])

#crops to remove uneccesary information
crop = img[320:390,400:900,:]

#divides out the average background, make sure this makes sense
crop_back = crop/ColorAverage(crop)

#Run each through their filters
redfloat = RedFilter(crop_back)
greenfloat = GreenFilter(crop_back)
bluefloat = BlueFilter(crop_back)


"""""""For loop for all frames"""""""""

#MASSIVE FOR LOOP FOR EVERY FRAME LET'S GO BABY
#data directories
#COM_write_path = ('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_COMs/')
#MED_write_path = ('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_MEDs/')
#STD_write_path = ('/home/miles/Desktop/Python/data/float_tracker/lightdiffused/6812_STDs/')


#for x in range(0,len(file_list)):
#    img = io.imread(file_list[x])
#    crop = img[320:390,400:900,:]
#    crop_back = crop/ColorAverage(crop)
#    
#    redfloat = RedFilter(crop_back)
#    greenfloat = GreenFilter(crop_back)
#    bluefloat = BlueFilter(crop_back)
#    
#    RGBCOM = np.array([COM(redfloat),COM(greenfloat),COM(bluefloat)])
#    np.savetxt(COM_write_path+'frame'+str(x)+'.out' ,RGBCOM.astype(int),fmt='%i')
#    

    


"""""""printouts:"""""""
print((redfloat[40,:]))
print("Red: ","COM:", COM(redfloat).astype(int), "STD:", xSTD(redfloat))
print("Green: ","COM:", COM(greenfloat).astype(int))
print("Blue: ", "COM:",COM(bluefloat).astype(int))

f, axarr = plt.subplots(2,2)
axarr[0,0].imshow(crop_back)
axarr[0,1].imshow(redfloat)
axarr[1,0].imshow(greenfloat)
axarr[1,1].imshow(bluefloat)