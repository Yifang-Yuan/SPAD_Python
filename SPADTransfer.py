#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 14:19:14 2021

@author: kurtulus
"""

import ok
import time
import numpy as np

class SPADTransfer():
    
    def __init__(self):    
        
        print('Welcome to SPADPhotometry!')
        self.dev = ok.okCFrontPanel()
        self.fp = ok.FrontPanel()
        self.info = ok.okTDeviceInfo()
   
            

    def GetDeviceName(self):
        name = self.dev.GetSerialNumber()
        print('Device Name is ', name)
        
    def TurnOnLED(self):
        self.dev.SetWireInValue(int(0),np.uint32(1))
        self.dev.UpdateWireIns()
        
    def TurnOffLED(self):
        self.dev.SetWireInValue(0,0)
        self.dev.UpdateWireIns()
        
    def SetVoltageLevels(self):
        self.dev.SetWireInValue(4,np.uint32(3.3*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(7,np.uint16(3.3*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(8,np.uint16(2.9*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(11,np.uint16(3.6*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(3,np.uint16(0.1*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(1,np.uint16(15.5*(1000/7.4)))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(5,np.uint16(1*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(6,np.uint16(1.2*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(10,np.uint16(1.1*1000))
        self.dev.UpdateWireIns()
        self.dev.SetWireInValue(0,1)
        self.dev.UpdateWireIns()
        

    

        
    def CheckLED(self):
        print(self.dev.GetWireInValue(1))
        
    
    def OpenCom(self):
        self.fp.OpenBySerial("")
        print(self.fp.IsOpen())
        if self.fp.IsOpen():
            print('Port is open')
        else:
            print('There are some errors! Check the port')
                
    def CloseCom(self):
        self.fp.Close()
        if not self.fp.IsOpen():
            print('Port is closed')
        else:
            print('Port could not be closed. There are some erors!')
            
    def CheckPort(self):
        
        if self.fp.IsOpen():
            print('Port is open')
        else:
            print('Port is closed')
            
    def UploadFile(self, file_name):
        
        error_open = self.dev.OpenBySerial("")
        if error_open == 0:
            print('Device is opened successfully')
        else:
            print(error_open)
        
        error = self.dev.ConfigureFPGA(file_name)
        
        if error == 0:
            print('Configuration was accomplished!')
            
        else:
            print(error)
        
    def StartAcquisition(self):
        
        error_open = self.dev.OpenBySerial("")
        
        if error_open == 0:
            
            while True:
                self.dev.UpdateWireOuts()
                data_1 = self.dev.GetWireOutValue(0x20)
                data_2 = self.dev.GetWireOutValue(0x21)
                data_3 = self.dev.GetWireOutValue(0x22)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print("time ={} counter {}".format(current_time, data_1))
                # time.sleep(0.001)
                
        else:
            print('There are some errors')
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

