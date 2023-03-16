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


#instantiate the sensor class
s = SPCIMAGER('SPCIMAGER_TOP.bit')

#connect to the sensor 
s.SensorConnect(s.bank)

#Start the sensor
s.SensorStart()

#Show the total photon counts from the sensor
s.ShowData()
