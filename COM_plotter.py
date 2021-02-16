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
from matplotlib.ticker import MultipleLocator
from mpl_toolkits import mplot3d
from stl import mesh
from mpl_toolkits.mplot3d import Axes3D
import cv2
import pandas as pd
import tables
import math

"""directories and data info"""
data_dir='/home/miles/Desktop/Python/data/float_tracker/switch/cycle/'
file_list=sorted(glob.glob(data_dir+'COMs/*.out'), key=os.path.getmtime)
img_file_list=sorted(glob.glob(data_dir+'frames/*.jpg'), key=os.path.getmtime)

frame_ratio = 1
camera_FPS=30
pixel_ratio=10.3  #pixels/mm
speed = 35/20 #mm/second
timestep = frame_ratio/camera_FPS*speed

"""functions"""
def ReadCOM(frame_ratio,frontcut,backcut):
    
    COM = np.zeros([3,2,int(len(file_list)/frame_ratio)])

    for x in range(frontcut,int(len(file_list)/frame_ratio)-backcut):
        frame_data = np.loadtxt(file_list[x*frame_ratio])
        COM[:,:,x] = frame_data
    return COM

def ReadMartin(xmult,xoff):
    data = np.loadtxt('/home/miles/Desktop/Python/data/float_tracker/MartinTaichi/taichi_data_for_miles2.txt')
    data = data*xmult
    data = data + xoff  

    return data

    
        
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
        
        
def GenerateVideoCheck(FPS):

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
    
def Plot():    
    # plt.subplot(1,2,1)
    
    # plt.scatter(-(COM[0,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed,color='r',marker='.')
    # plt.scatter(-(COM[1,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed, color='g',marker='.')
    plt.scatter(-(COM[2,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed,color='b',marker='.')
    
    """filter outliers for line plot"""
    
    
    # plt.plot(-(COM[0,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed,color='r')
    # plt.plot(-(COM[1,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed, color='g')
    # plt.plot(-(COM[2,1,:].astype(int)/pixel_ratio)+60,(np.arange(0,len(COM[0,0,:])*timestep,timestep))-31*speed,color='b')

    

    # plt.title('')
    # plt.ylabel('Z-distance (mm)',fontsize = 24) 
    # plt.xlabel('X-distance (mm)',fontsize = 24)
    # plt.ylim(56*speed,0)
    # plt.yticks(fontsize = 15)
    # plt.xlim(0,45)
    # plt.xticks(fontsize = 15)

    
    # plt.subplot(1,2,2)
    
    # xmult = -9.9
    # xoff = 26.4
    # ymult = 4
    # yoff = 0
    
    # martx1 = ReadMartin(xmult,xoff)[:,0]
    # martx2 = ReadMartin(xmult,xoff)[:,2]
    # martx3 = ReadMartin(xmult,xoff)[:,4]
    # marty1 = ReadMartin(ymult,yoff)[:,1]
    # marty2 = ReadMartin(ymult,yoff)[:,3]
    # marty3 = ReadMartin(ymult,yoff)[:,5]

    # plt.plot(martx1,np.arange(0,len(martx1)/ymult,1/ymult)+yoff, color='tomato')
    # plt.plot(martx2,np.arange(0,len(martx2)/ymult,1/ymult)+yoff, color='limegreen')
    # plt.plot(martx3,np.arange(0,len(martx3)/ymult,1/ymult)+yoff, color='cornflowerblue')
    
    # plt.title('')
    # plt.ylabel('Z-distance (mm)',fontsize = 24) 
    # plt.xlabel('X-distance (mm)',fontsize = 24)
    # plt.ylim(56*speed,0)
    # plt.yticks(fontsize = 15)
    # plt.xlim(0,100)
    # plt.xticks(fontsize = 15)

    fig = plt.gcf()
    fig.set_size_inches(5,10)
    plt.tight_layout()
    name = "SCATcycle"
    plt.savefig('/home/miles/Desktop/Python//float_tracker/plots/{}.svg'.format(name))
    plt.savefig('/home/miles/Desktop/Python//float_tracker/plots/{}.png'.format(name))
    plt.savefig('/home/miles/Desktop/Python//float_tracker/plots/{}.pdf'.format(name))
    plt.show()
  
def PlotMartin():
    xmult = -1
    xoff = 0
    ymult = 1
    yoff = 0
    martx1 = ReadMartin(xmult,xoff)[:,0]
    martx2 = ReadMartin(xmult,xoff)[:,2]
    martx3 = ReadMartin(xmult,xoff)[:,4]
    # marty1 = ReadMartin(ymult,yoff)[:,1]
    # marty2 = ReadMartin(ymult,yoff)[:,3]
    # marty3 = ReadMartin(ymult,yoff)[:,5]

    plt.plot(martx1,np.arange(0,len(martx1)/ymult,1/ymult)+yoff)
    plt.plot(martx2,np.arange(0,len(martx2)/ymult,1/ymult)+yoff)
    plt.plot(martx3,np.arange(0,len(martx3)/ymult,1/ymult)+yoff)
    
    plt.title('')
    plt.ylabel('Z-distance (mm)',fontsize = 24) 
    plt.xlabel('X-distance (mm)',fontsize = 24)
    # plt.ylim(56*speed,0)
    # plt.yticks(fontsize = 15)
    # plt.xlim(0,45)
    # plt.xticks(fontsize = 15)

    fig = plt.gcf()
    fig.set_size_inches(10,10)
    plt.tight_layout()
    plt.savefig('/home/miles/Desktop/martinplot.png', dpi=500)
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
    
    
# def Dphi(COM,i,northpole,southpole):
#     phi1 = np.arctan2(COM[southpole,1,i-1]-COM[northpole,1,i-1],COM[southpole,0,i-1]-COM[northpole,0,i-1])
#     phi2 = np.arctan2(COM[southpole,1,i]-COM[northpole,1,i],COM[southpole,0,i]-COM[northpole,0,i])
#     dphi = phi1-phi2
    
#     return dphi

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
    
    # plt.title('Experiment vs Theory: Both Directions')
    # plt.ylabel('Angular Displacement (radians)',fontsize = 12) 
    # plt.xlabel('Time (seconds)',fontsize = 12)
    # plt.axis('off')

    
    plt.yticks(np.arange(-2*math.pi,2*math.pi,math.pi/4))

    plt.tick_params(
    axis='both',
    which='both', 
    direction = 'in',
    bottom=True,
    top=False,
    labelleft=True,
    labelbottom=True)
    
    plt.axes().xaxis.set_minor_locator(MultipleLocator(10))
     
    
    #full cycles
    # plt.scatter((np.arange(0,len(phi)*timestep,timestep)),phi,s=1)
    
    #3 cycles
    # xmin = int(102/timestep)
    # xmax = int(332/timestep)
    # plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin:xmax]-xmin*timestep,phi[xmin:xmax]-phi[xmin],s=4)

    #ratchet
    # xmin = int(102/timestep)
    # xmax = int(145/timestep)
    #plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin:xmax]-xmin*timestep,phi[xmin:xmax]-phi[xmin])
    
    #ratchet vs martin
    xmin = int(107/timestep)
    xmax = int(123/timestep)
    # plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin:xmax]-xmin*timestep,-1*phi[xmin:xmax]+phi[xmin], label="experiment: ratchet",marker='.',s=4)
    plt.plot((np.arange(0,len(phi)*timestep,timestep))[xmin:xmax]-xmin*timestep,-1*phi[xmin:xmax]+phi[xmin], label="experiment: ratchet")
    
    #twist
    # xmin2 = int(140/timestep)
    # xmax2 = int(182/timestep)
    # plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin2:xmax2]-xmin2*timestep-xmin*timestep,phi[xmin2:xmax2]-phi[xmin2],s=0.5)
    
    #twist vs martin
    xmin2 = int(162/timestep)
    xmax2 = int(178/timestep)
    # plt.scatter((np.arange(0,len(phi)*timestep,timestep))[xmin2:xmax2]-xmin2*timestep,phi[xmin2:xmax2]-phi[xmin2], label="experiment: twist",marker='.',s=4)
    plt.plot((np.arange(0,len(phi)*timestep,timestep))[xmin2:xmax2]-xmin2*timestep,phi[xmin2:xmax2]-phi[xmin2], label="experiment: twist")
    
    # #martin 
    martindata = pd.read_csv("/home/miles/Desktop/Python/data/float_tracker/Martin/Martin-numerical-results.csv")
    channeltimeratio = 5
    # plt.scatter(martindata["x"]*channeltimeratio,martindata["rotating"], label="theory: twist",marker='.',s=4)
    # plt.scatter(martindata["x"]*channeltimeratio,martindata["ratcheting"], label="theory: ratchet",marker='.',s=4)
    plt.plot(martindata["x"]*channeltimeratio,martindata["rotating"], label="theory: twist")
    plt.plot(martindata["x"][0:34]*channeltimeratio,martindata["ratcheting"][0:34], color='r', label="theory: ratchet")
    plt.plot(martindata["x"][35:60]*channeltimeratio,martindata["ratcheting"][35:60], color='r')
    
    # plt.ylim(-1.7,1.7)

    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(4,4)
    plt.tight_layout()
    plt.savefig('/home/miles/Desktop/Python//float_tracker/plots/LINEbothvsmartin.png')
    plt.savefig('/home/miles/Desktop/Python//float_tracker/plots/LINEbothvsmartin.svg')
    plt.savefig('/home/miles/Desktop/Python//float_tracker/plots/LINEbothvsmartin.pdf')
    plt.show()
    
    
def Plot3D(COM,tmin,tmax,Azim,Elev,path,DPI): 
    fig = plt.figure()
    ax = Axes3D(fig, rect=None, azim=Azim-90, elev=Elev)
    
    plt.ylabel('Y-distance (mm)',fontsize = 14) 
    plt.xlabel('X-distance (mm)',fontsize = 14)
    plt.xlim(0,45)
    plt.ylim(31,76)
    
    zmin = int(tmin/timestep)
    zmax = int(tmax/timestep)
    
    xdata = -(COM[0,1,zmin:zmax].astype(int)/pixel_ratio)+60
    ydata = -(COM[0,0,zmin:zmax].astype(int)/pixel_ratio)+60
    zdata = (np.arange(0,len(COM[0,0,zmin:zmax])*timestep,timestep))
    ax.scatter(xdata,ydata,-zdata, color='r', marker='.')
    
    xdata = -(COM[1,1,zmin:zmax].astype(int)/pixel_ratio)+60
    ydata = -(COM[1,0,zmin:zmax].astype(int)/pixel_ratio)+60
    zdata = (np.arange(0,len(COM[1,0,zmin:zmax])*timestep,timestep))
    ax.scatter(xdata,ydata,-zdata, color='g', marker='.')
    
    xdata = -(COM[2,1,zmin:zmax].astype(int)/pixel_ratio)+60
    ydata = -(COM[2,0,zmin:zmax].astype(int)/pixel_ratio)+60
    zdata = (np.arange(0,len(COM[2,0,zmin:zmax])*timestep,timestep))
    ax.scatter(xdata,ydata,-zdata, color='b', marker='.')

    
    fig.set_size_inches(10,12)
    plt.tight_layout()
    plt.savefig(path, dpi=DPI)
    # plt.show()
    
def AnimatePlot3D(COM,tmin,tmax,Elev,azimrange,azimstepsize,DPI):
    for x in range(0,azimrange,azimstepsize):
        Plot3D(COM,tmin,tmax,x,Elev,data_dir+'3dSweep/%d.png' % x,DPI)
    
    
def PlotSTL():
    # Not working fully -- can't figure out how to translate the stl, and it's at weird coordinates
    fig = plt.figure()
    ax = Axes3D(fig)
    
    plt.ylabel('Y-distance (mm)',fontsize = 14) 
    plt.xlabel('X-distance (mm)',fontsize = 14)
    plt.xlim(1000,1200)
    plt.ylim(0,200)

    # Load the STL files and add the vectors to the plot
    your_mesh = mesh.Mesh.from_file(data_dir+'Taichi.stl')
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors,alpha=0.2))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten('K')
    ax.auto_scale_xyz(scale, scale, scale/10)
    
    print(your_mesh)
    plt.show()
    
    

    
""""""""""""
COM = ReadCOM(frame_ratio,0,0)
#GenerateAllFramesCOMCheck(5,frame_ratio)
#GenerateAllFramesAngleCheck(5,frame_ratio,0,2)
Plot()
# PlotAngle(COM,2,0)
#PlotAngleDisplacement(COM,0,2)
#Plot3D(COM,31*speed,87*speed,20,20,data_dir+'3dtaichi_20ang_20elev.png',300)
#AnimatePlot3D(COM,31*speed,87*speed,20,90,1,100)
#PlotSTL()
#print(Dphi(250,2,0))
#CheckFrame(0,0)
#print(COM[:,:,338])
#AngleCheck(0,0,2)
#GenerateVideoCheck(10)