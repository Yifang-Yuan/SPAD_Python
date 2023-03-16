#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:12:20 2022

@author: kurtulus
"""

"""
Script for test the sensor. 

"""



from SPCIMAGERAA import SPCIMAGER
from SPADAnalysis import SPADAnalysis

#instantiate the sensor class
s = SPCIMAGER('SPCIMAGER_TOP.bit')

#connect to the sensor 
s.SensorConnect(s.bank)

#Start the sensor
s.SensorStart()

recording_time = int(input("Please enter the duration of the recording: "))

#Show the total photon counts from the sensor
s.RecordData(recording_time)



#p = SPADAnalysis("sample.bin", recording_time)

s.SensorDisconnect()




