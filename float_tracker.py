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


"""""""""Functions"""""""""""
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
    
    redsignal = abs(image[:,:,0]-floatcoloraverage[0]) < floatcolorSTD[0]*redcutoff
    greensignal = abs(image[:,:,1]-floatcoloraverage[1]) < floatcolorSTD[1]*greencutoff
    bluesignal = abs(image[:,:,2]-floatcoloraverage[2]) < floatcolorSTD[2]*bluecutoff
    fullmatch = np.logical_and(redsignal,greensignal,bluesignal)
    
    filtered[fullmatch]=1
    return filtered



"""The following will need to be tweaked manually for each analysis. 
It is crucial that for each video, you do the supercrop around each float to establish the float colors"""
#read data
img = io.imread('/home/miles/Desktop/Python/data/6794/scene00001.png')

#crops to remove uneccesary information
crop = img[300:400,500:900,:]

#get colors of each float
supercrop_redfloat = crop[45:60,60:70,:]
supercrop_yellowfloat = crop[45:65,260:280,:]
supercrop_bluefloat = crop[45:60,290:300,:]

#set filter thresholds, each value is the number of 
#standard deviations from the mean value of each channel of the supercrop of each float
redcutoff = 1
greencutoff = 1
bluecutoff = 1


"""""""business end"""""""""
coloraverage = ColorAverage(crop)
colorSTD = ColorSTD(crop)

redfloat = Filter(crop,supercrop_redfloat)
yellowfloat = Filter(crop,supercrop_yellowfloat)
bluefloat = Filter(crop,supercrop_bluefloat)

"""""""printouts:"""""""

print("redCOM: ", COM(redfloat))
print("yellowCOM: ", COM(yellowfloat))
print("blueCOM: ", COM(bluefloat))

f, axarr = plt.subplots(2,2)
axarr[0,0].imshow(crop)
axarr[0,1].imshow(redfloat)
axarr[1,0].imshow(yellowfloat)
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