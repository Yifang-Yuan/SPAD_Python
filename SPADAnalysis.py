#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 14:17:24 2022

@author: kurtulus
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


class SPADAnalysis():
    
        def __init__(self, binfile, no_of_bitplanes):
            
            
            self.file = binfile
            dtype = np.dtype('B')
            try:
                with open(self.file, "rb") as f:
                    self.numpy_data = np.fromfile(f,dtype)
                    print(self.numpy_data)
            except IOError:

                print('Error While Opening the file!') 
        
            
            self.matrix_data = self.numpy_data.reshape((no_of_bitplanes, -1))
            
            
            #assumes mat_data is 2D matrix which is frames as rows
            #and byte values from sensor as columns
            
            trace = self.matrix_data.sum(axis =1)
            
            time =np.arange(0,no_of_bitplanes)/10000
            plt.figure(figsize = (10,10))
            plt.plot(time, trace)
            plt.xlabel("Recording Time(seconds)")
            plt.ylabel("Total Photon Counts")
            today = dt.date.today().strftime("%b-%d-%Y"),
            name = "recording_" + str(today)
            plt.savefig(name, format = 'png')
            
            
            
            
            
            
            
            
            
            
            
            
            
            