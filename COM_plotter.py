#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 11:33:17 2019


Remember that the COM data structure is [RGB,YX,FRAME], so if you want the X coordinate of the 
red float on the 69th frame, you type COM[0,1,69]
@author: miles
"""

import numpy as np
import glob
import os
from skimage import io
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import cv2
import pandas as pd

"""directories and data info"""
data_dir='/home/miles/Desktop/Python/data/float_tracker/ratchet3/'
file_list=sorted(glob.glob(data_dir+'COMs/*.out'), key=os.path.getmtime)
img_file_list=sorted(glob.glob(data_dir+'frames/*.jpg'), key=os.path.getmtime)

frame_ratio = 1
camera_FPS=30
pixel_ratio=10.3  #pixels/mm
speed = 35/20 #mm/second
timestep = frame_ratio/camera_FPS*speed

"""functions"""
def ReadCOM(frame_ratio):
    
    COM = np.zeros([3,2,int(len(file_list)/frame_ratio)])

    for x in range(0,int(len(file_list)/frame_ratio)):
        frame_data = np.loadtxt(file_list[x*frame_ratio])
        COM[:,:,x] = frame_data
    return COM
        
def CheckFrame(frame,channel):
    img = io.imread(img_file_list[frame])
    img = img[350:520,590:750,:] #use same cropping as you did in float_tracker.py!!!
    
    frame_data = np.loadtxt(file_list[frame])
    COM = frame_data
    
    plt.imshow(img)
    plt.scatter(COM[channel,1],COM[channel,0])
    
    plt.show()
    print(COM[channel])
 
def AngleCheck(frame,northpole,southpole):
    img = io.imread(img_file_list[frame])
    img = img[350:520,590:750,:] #use same cropping as you did in float_tracker.py!!!
    frame_data = np.loadtxt(file_list[frame])
    COM = frame_data
    
    plt.imshow(img)
    plt.arrow(COM[northpole,1],COM[northpole,0],COM[southpole,1]-COM[northpole,1],COM[southpole,0]-COM[northpole,0],color='yellow',linewidth=5,head_width=2)
    
    plt.show()

    
def GenerateAllFramesCOMCheck(FPS,frame_ratio):
    for x in range(0,int(len(file_list)/frame_ratio)):
        img = io.imread(img_file_list[x*frame_ratio])
        img = img[350:520,590:750,:] #use same cropping as you did in float_tracker.py!!!
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
        img = img[350:520,590:750,:] #use same cropping as you did in float_tracker.py!!!
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
    
def Plot(COM):
    plt.title('')
    plt.ylabel('Z-distance (mm)',fontsize = 24) 
    plt.xlabel('X-distance (mm)',fontsize = 24)
    plt.ylim(56*speed,0)
    plt.yticks(fontsize = 15)
    plt.xlim(0,45)
    plt.xticks(fontsize = 15)
    plt.scatter(-(COM[0,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed,color='r',marker='.')
    plt.scatter(-(COM[1,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed, color='g',marker='.')
    plt.scatter(-(COM[2,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed,color='b',marker='.')
#    plt.plot(COM[0,1,:].astype(int),(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS,frame_ratio/camera_FPS)),color='r')
#    plt.plot(COM[1,1,:].astype(int),(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS,frame_ratio/camera_FPS)), color='g')
#    plt.plot(COM[2,1,:].astype(int),(np.arange(0,len(COM[0,0,:])*frame_ratio/camera_FPS,frame_ratio/camera_FPS)),color='b')    
    

    fig = plt.gcf()
    fig.set_size_inches(5,10)
    plt.tight_layout()
    plt.savefig(data_dir+'paper_fig2D_2.png', dpi=300)
    plt.savefig('paper_fig2D_2.png', dpi=300)
    plt.show()
    
    
def PlotAngle(COM,northpole,southpole):
    
    phi = np.arctan2(COM[southpole,1]-COM[northpole,1],COM[southpole,0]-COM[northpole,0])+np.pi
    
    plt.title('')
    plt.ylabel('Angle (radians)',fontsize = 24) 
    plt.xlabel('Time (seconds)',fontsize = 24)
    
    plt.scatter((np.arange(0,len(phi)*timestep,timestep)),phi, marker='.')
    
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    plt.tight_layout()
    plt.savefig(data_dir+'angleplot.png', dpi=300)
    plt.show()
    
    
def Dphi(i,northpole,southpole):
    phi1 = np.arctan2(COM[southpole,1,i-1]-COM[northpole,1,i-1],COM[southpole,0,i-1]-COM[northpole,0,i-1])
    phi2 = np.arctan2(COM[southpole,1,i]-COM[northpole,1,i],COM[southpole,0,i]-COM[northpole,0,i])
    dphi = phi1-phi2
    
    return dphi

def PlotAngleDisplacement(COM,northpole,southpole):
    """Get the angles, and let it go past 2pi by looking for the jump back to 0 and adding 2pi for each rotation"""
    rotations=0
    phi=np.zeros(len(COM[0,0,:]))
    for i in range(0,len(COM[0,0,:])):
        phi1 = np.arctan2(COM[southpole,1,i-1]-COM[northpole,1,i-1],COM[southpole,0,i-1]-COM[northpole,0,i-1])
        phi2 = np.arctan2(COM[southpole,1,i]-COM[northpole,1,i],COM[southpole,0,i]-COM[northpole,0,i])
        if (abs(phi2-phi1)>3):
            rotations=rotations+1
            print(rotations)
        phi[i]=phi2+rotations*2*np.pi

    """plotting grounds"""
    
    plt.title('Experiment vs Theory: Both Directions')
    plt.ylabel('Angular Displacement (radians)',fontsize = 24) 
    plt.xlabel('Time (seconds)',fontsize = 24)
    #plt.ylim(-3,3)
    

#    #ratchet
#    xmin = int(102/timestep)
#    xmax = int(145/timestep)
#    plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin:xmax]-xmin*timestep,phi[xmin:xmax]-phi[xmin])
    
    #ratchet vs martin
    xmin = int(107/timestep)
    xmax = int(123/timestep)
    plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin:xmax]-xmin*timestep,-1*phi[xmin:xmax]+phi[xmin], label="experiment: ratchet")
    
#    #twist
#    xmin2 = int(140/timestep)
#    xmax2 = int(182/timestep)
#    plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin2:xmax2]-xmin2*timestep-xmin*timestep,phi[xmin2:xmax2]-phi[xmin2])
    
    #twist vs martin
    xmin2 = int(162/timestep)
    xmax2 = int(178/timestep)
    plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin2:xmax2]-xmin2*timestep,phi[xmin2:xmax2]-phi[xmin2], label="experiment: twist")

    #martin 
    martindata = pd.read_csv("/home/miles/Desktop/Python/data/float_tracker/Martin/Martin-numerical-results.csv")
    channeltimeratio = 5
    plt.scatter(martindata["x"]*channeltimeratio,martindata["rotating"], marker='o', label="theory: twist")
    plt.scatter(martindata["x"]*channeltimeratio,martindata["ratcheting"], marker='o', label="theory: ratchet")

    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    plt.tight_layout()
    plt.savefig(data_dir+'angleplotdisp_exptheorycomparisonboth.png', dpi=300)
    plt.show()
    
    
def Plot3D(COM,tmin,tmax): 
    ax = plt.axes(projection='3d')
    plt.ylabel('y')
    plt.xlabel('x')
    # plt.ylim(50,60)
    # plt.xlim(40,60)
    
    zmin = int(tmin/timestep)
    zmax = int(tmax/timestep)
    
    xdata = -(COM[0,1,zmin:zmax].astype(int)/pixel_ratio)+60
    ydata = -(COM[0,0,zmin:zmax].astype(int)/pixel_ratio)+60
    zdata = (np.arange(0,len(COM[0,0,zmin:zmax])*timestep,timestep))-31*speed
    ax.scatter3D(xdata,ydata,zdata, color='r', marker='.')
    
    # xdata = -(COM[1,1,zmin:zmax].astype(int)/pixel_ratio)+60
    # ydata = -(COM[1,0,zmin:zmax].astype(int)/pixel_ratio)+60
    # zdata = (np.arange(0,len(COM[0,0,zmin:zmax])*timestep,timestep))-31*speed
    # ax.scatter3D(xdata,ydata,zdata, color='g', marker='.')
    
    xdata = -(COM[2,1,zmin:zmax].astype(int)/pixel_ratio)+60
    ydata = -(COM[2,0,zmin:zmax].astype(int)/pixel_ratio)+60
    zdata = (np.arange(0,len(COM[0,0,zmin:zmax])*timestep,timestep))-31*speed
    ax.scatter3D(xdata,ydata,zdata, color = 'b', marker='.')


    
""""""""""""
COM = ReadCOM(frame_ratio)
#GenerateAllFramesCOMCheck(5,frame_ratio)
#GenerateAllFramesAngleCheck(5,frame_ratio,0,2)
#Plot(COM)
#PlotAngle(COM,2,0)
#PlotAngleDisplacement(COM,0,2)
Plot3D(COM,100,200)
#print(Dphi(250,2,0))
#CheckFrame(0,0)
#print(COM[:,:,338])
#AngleCheck(0,0,2)