#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 14:43:47 2021

@author: miles
"""
import glob
import os

"""directories and data info"""
data_dir='/home/miles/Desktop/Python/data/float_tracker/switch/cycle/'
file_list=sorted(glob.glob(data_dir+'COMs/*.out'), key=os.path.getmtime)



with open(data_dir+'fullCOMs','w') as outfile:
    for fname in file_list:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
                