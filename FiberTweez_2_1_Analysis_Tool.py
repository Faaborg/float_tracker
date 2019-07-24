#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 11:47:15 2018

@author: miles
"""



#Import
import numpy as np
from scipy import ndimage
from skimage import io
import matplotlib.pyplot as plt

"""Define functions"""
def COM(data):
    if data.ndim==3:
        com = np.zeros((len(data[:]),2))
        for x in range(0,len(data[:])):
            temp = data[x,:,:]
            temp[temp<50] = 0
            temp[temp>=50] = 200
            com[x,:] = ndimage.measurements.center_of_mass(temp[:,:])
    else:
        data[data<50] = 0
        data[data>=50] = 200
        com = ndimage.measurements.center_of_mass(data)
    return com

def DEF(data,zero):
    deflection = np.zeros((len(data[:])))
    for x in range(0,len(data[:])):
        deflection[x] = ((zero[1]-data[x,1])**2 + (zero[0]-data[x,0])**2)**(1/2)
    return deflection

"""Set parmeters that don't change between runs (function not needed)"""

length = 134 #length in mm
pixel = 0.93 #pixels per um, as measured by imagej
femptok = 0.0485*(80/length)**3 #using the k-value measured from the 80mm femptotool analysis
speed = 50 #translation speed of the plate in microns per second
fps = 10 #fps of camera
deltaD = speed/fps #um between each frame
Dstart = 6000 #starting distance from zero in microns
Dend = 2000 #ending distance from zero in microns


"""Read in data"""
data_dir = ('/home/miles/Desktop/Python/data/exp2/') #point to experiment

adv1 = np.concatenate((io.imread(data_dir+'adv1.tif')[:,:,:,0], io.imread(data_dir+'adv1_0.tif')[:,:,:,0], io.imread(data_dir+'adv1_1.tif')[:,:,:,0], io.imread(data_dir+'adv1_2.tif')[:,:,:,0]))
adv2 = np.concatenate((io.imread(data_dir+'adv2.tif')[:,:,:,0], io.imread(data_dir+'adv2_0.tif')[:,:,:,0], io.imread(data_dir+'adv2_1.tif')[:,:,:,0], io.imread(data_dir+'adv2_2.tif')[:,:,:,0]))
adv3 = np.concatenate((io.imread(data_dir+'adv3.tif')[:,:,:,0], io.imread(data_dir+'adv3_0.tif')[:,:,:,0], io.imread(data_dir+'adv3_1.tif')[:,:,:,0], io.imread(data_dir+'adv3_2.tif')[:,:,:,0]))

rec1 = np.concatenate((io.imread(data_dir+'rec1.tif')[:,:,:,0], io.imread(data_dir+'rec1_0.tif')[:,:,:,0], io.imread(data_dir+'rec1_1.tif')[:,:,:,0], io.imread(data_dir+'rec1_2.tif')[:,:,:,0]))
rec2 = np.concatenate((io.imread(data_dir+'rec2.tif')[:,:,:,0], io.imread(data_dir+'rec2_0.tif')[:,:,:,0], io.imread(data_dir+'rec2_1.tif')[:,:,:,0], io.imread(data_dir+'rec2_2.tif')[:,:,:,0]))
rec3 = np.concatenate((io.imread(data_dir+'rec3.tif')[:,:,:,0], io.imread(data_dir+'rec3_0.tif')[:,:,:,0], io.imread(data_dir+'rec3_1.tif')[:,:,:,0], io.imread(data_dir+'rec3_2.tif')[:,:,:,0]))


zero1 = io.imread('/home/miles/Desktop/Python/data/calibrations/25mm after.tif')
zero2 = io.imread('/home/miles/Desktop/Python/data/calibrations/25mm after.tif')
zero3 = io.imread('/home/miles/Desktop/Python/data/calibrations/25mm after.tif')
zero = np.array((COM(zero1[:,:,0]),COM(zero2[:,:,0]),COM(zero3[:,:,0]))).mean(0)
#Load all 3 pictures, then take COM of just the red channel and then average together the elements.

"""business end"""

"""advancing"""
#Going to either have to make assumptions. For advancing, let's add 2 seconds of Dstart to the front, and then 
#take argmax of force to be Dend, and then add len-argmax of Dend on the end. Then, we'll just devide the rest by 
#what needs to be divided by, and make sure that it's very close to 'speed'

adv1_com = COM(adv1)
adv1_def = DEF(adv1_com,zero)
adv1_force = adv1_def / pixel * femptok #in uN
adv1_x = np.linspace(Dstart,Dend,np.argmax(adv1_force)-2*speed)
adv1_x = np.concatenate((np.ones(2*speed)*Dstart,adv1_x,(np.ones(len(adv1_force)-np.argmax(adv1_force))*Dend)))

adv2_com = COM(adv2)
adv2_def = DEF(adv2_com,zero)
adv2_force = adv2_def / pixel * femptok #in uN
adv2_x = np.linspace(Dstart,Dend,np.argmax(adv2_force)-2*speed)
adv2_x = np.concatenate((np.ones(2*speed)*Dstart,adv2_x,(np.ones(len(adv2_force)-np.argmax(adv2_force))*Dend)))

adv3_com = COM(adv3)
adv3_def = DEF(adv3_com,zero)
adv3_force = adv3_def / pixel * femptok #in uN
adv3_x = np.linspace(Dstart,Dend,np.argmax(adv3_force)-2*speed)
adv3_x = np.concatenate((np.ones(2*speed)*Dstart,adv3_x,(np.ones(len(adv3_force)-np.argmax(adv3_force))*Dend)))


"""receding"""
#For this, just look at the data and see at whata point it starts moving. Toss those points all together.
rec1_com = COM(rec1)
rec1_def = DEF(rec1_com,zero)
rec1_force = rec1_def / pixel * femptok #in uN
rec1_trunk = np.delete(rec1_force,np.arange(30)) #CHOOSE FOR EACH FILE HOW MANY POINTS TO TOSS
rec1_x = np.linspace(Dend,Dstart, len(rec1_trunk))

rec2_com = COM(rec2)
rec2_def = DEF(rec2_com,zero)
rec2_force = rec2_def / pixel * femptok
rec2_trunk = np.delete(rec2_force,np.arange(30))
rec2_x = np.linspace(Dend,Dstart, len(rec2_trunk))

rec3_com = COM(rec3)
rec3_def = DEF(rec3_com,zero)
rec3_force = rec3_def / pixel * femptok
rec3_trunk = np.delete(rec3_force,np.arange(30))
rec3_x = np.linspace(Dend,Dstart, len(rec3_trunk))

"""out"""
np.savetxt(data_dir+'adv1_x.out' , adv1_x)
np.savetxt(data_dir+'adv2_x.out' , adv2_x)
np.savetxt(data_dir+'adv3_x.out' , adv3_x)

np.savetxt(data_dir+'adv1_force.out' , adv1_force)
np.savetxt(data_dir+'adv2_force.out' , adv2_force)
np.savetxt(data_dir+'adv3_force.out' , adv3_force)

np.savetxt(data_dir+'rec1_x.out' , rec1_x)
np.savetxt(data_dir+'rec2_x.out' , rec2_x)
np.savetxt(data_dir+'rec3_x.out' , rec3_x)

np.savetxt(data_dir+'rec1_force.out' , rec1_trunk)
np.savetxt(data_dir+'rec2_force.out' , rec2_trunk)
np.savetxt(data_dir+'rec3_force.out' , rec3_trunk)
