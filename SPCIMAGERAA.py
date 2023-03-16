

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 22:54:11 2021
@author: kurtulus
SPCIMAGER is a class which contains the necessary methods for operating the sensor. 
Initial method contains basic set-up for PCB. 
"""

import numpy as np
import ok
from OK_Comms import OK_Comms
import time
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Scope import Scope

from datetime import datetime

class SPCIMAGER():
    
    def __init__(self, bitfile):
        
        print('Welcome to SPADPhotometry!')

        self.com = OK_Comms() 
        
        
        self.FPNCorrection = np.zeros((240,320))
        self.FPNCorrectionMask = np.ones((240,320))
        
        
        #System Settings
        
        self.ClockFreq = 50e6
        self.DigClockFreq = 50e6
        
        
        #Pulse Generators
        
        self.BinAPos1 = 0
        self.BinAPos2 = 10
        
        self.BinBPos1 = 0
        self.BinPos2 = 0
        
        self.BinADAC = 15
        self.BinBDAC = 15
        
        
        
        #Power Supplies default values:
        self.VDDE = 3.3 #External VDDE
        self.V1V2 = 1.2 # GO1 Logic
        self.V3V3 = 3.3 #GO2 Logic
        self.V3V6 = 3.6 # Time Gate & Reset Buffer VDD
        self.V2V7 = 2.7 # Pixel Array VDD
        self.VDDOPAMP = 3.3
        self.ADCPWR = 3.3
        self.VREF = 1.0
        
        self.VHV = 15.5 # Main Array
        self.VHV2 = 13.0 # Test Pixels
        
        self.ExposureTime = 1
        self.ExposureMode = 0
        
        self.NoOfExposures = 1
        self.PixelBit = 1
        
        # ---------------------
        # Bias Voltages
        self.VG = 3.3
        self.VS = 0.1
        self.VQ = 1
        
        self.DAC5 = 0 # Spare
        self.DAC6 = 0 # Spare
        
        # Current Biases:
        self.IBIAS1 = 3 # 2.72V into a 270K res = 10uA, JP47
        self.IBIAS2 = 1.1 # 2.72V into a 270K res = 10uA, JP68
        
        
        #Pulse generators
        
        self.BinAOutput = 'Disabled'
        self.BinBOutput = 'Disabled'
        
        self.BinAInputSel = 'PulseGen'
        self.BinBInputSel = 'PulseGen'
        
        self.OptClkOffsetSel = 'Low'
        
        
        
        self.PixelsActive = 'SPC'
        
        self.RowMin = 1
        self.RowMax = 240
        
        
        self.ColMin = 0
        self.ColMax = 319
        
        self.OutputMode = 'Analogue'
        self.CaptureMode = 'Single'
        
        self.CDS = 'On'
        self.Crowbar = 'On'
        
        self.GlobalReset = 'Off'
        
        self.DigitalTOFAmbientRejection = 'Off'
        
        self.RollingResetTime = 100
        self.GlobalResetTime = 20
        
        self.ColumnScanOutTime = 59
        self.ADC_Signal_Sample_Start = 27
        self.ADC_Crowbar_Sample_Start = 54
        
        self.CDSTime = 30
        
        
        
        self.SensorStatus = 'Disconnected'
        self.SensorMode = 'Off'
        
        self.SensorRevision = 'SPCIMAGER_AB'
        
        self.com.ok_header_func(bitfile)
        
        self.bank = self.com.bank
        
        
        
        
        
        
        
    def SensorConnect(self, bank):
        
        if self.SensorStatus == 'Connected':
            print('***WARNING: Sensor already connected')
            return
        
        self.SensorStatus = 'Connected'
        self.SensorMode = 'Idle'
        
        
        f = self.com.wireoutdata(bank, 'FIRMWARE_REVISION')
        print('*Firmware Revision: ', f)
        
        self.com.wireindata(bank, 'SPCIMAGER_CHIP_RESET', 1)
        
        self.SensorStartUpVoltages(0.00) 
        
        self.com.wireindata(bank, 'SPCIMAGER_CHIP_RESET', 0)
        
        self.SetCrowbar('On')
        
        self.SetExposures(1,1)
        
        self.com.wireindata(bank, 'ADC_PU', 1)
        
        
        self.SetTimeGateInput('Bin A', 'ExtClk','High')
        self.SetTimeGateInput('Bin B', 'ExtClk', 'High')
        self.SetExposureTime(self.ExposureTime)
        
        self.SetExposureMode(0)
        
        
        self.SetRegionOfInterest(self.RowMin, self.RowMax, self.ColMin, self.ColMax)
        
        self.SetResetTime(self.RollingResetTime, self.GlobalResetTime)
        
        self.SetColumnScanOutTime(self.ColumnScanOutTime, self.ADC_Signal_Sample_Start, self.ADC_Crowbar_Sample_Start)
        
        self.SetCDSTime(self.CDSTime)
        
        self.SetDigitalTOFAmbientRejection(self.DigitalTOFAmbientRejection)
        
        self.com.trigger(bank, 'ADC_FIFO_RST')
        
        
        self.SetSensorRevision(self.SensorRevision)
        
        
        print('*Connected to Sensor')
        
        
        
        self.com.trigger(bank, 'PROG_CTRL_SR')
        
        
        print('* Ready for operation')
        
        
        
    def ConnectCheck(self):
        
        if self.SensorStatus == 'Disconnected':
            print('***ERROR: Sensor not connected')
            return 
        
    def SensorStart(self):
        
        self.SetExposureMode(6)
        self.SetVoltage('VG', 3.3)
        self.SetVoltage('V3V3', 3.3)
        self.SetVoltage('V2V7', 2.9)
        self.SetVoltage('V3V6', 3.6)
        
        self.SetVoltage('VS', 0.1)
        self.SetVoltage('VHV', 15.5)
        self.SetVoltage('VQ', 1)
        self.SetVoltage('VREF', 1.2)
        self.SetVoltage('IBIAS2', 1.1)
        self.SetExposureTime(100.32)
        self.SetResetTime(20,100)
        
        self.gexp = 0
        self.b_saved = 0
        self.g_back = 0
        self.exptime = 100
        self.bright = 1
        self.com.wireindata(self.bank, 'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE', 1)
        self.n = 1
        self.y1 = 1
        self.y2 = 240
        self.file_name = 'spc_data'
        self.blocks = 1
        self.bitplanes = 10000
        self.stop = 0
        
        self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 1)
        time.sleep(0.1)
        self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 0)
        self.com.trigger(self.bank, 'PROG_CTRL_SR')
        
        
        
     
        
    def GetLiveData(self):
        
        
            last_points =[]
            #while 1:
        
            gexp = self.gexp
            self.com.wireindata(self.bank, 'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE', 1-gexp)
            
            exptime = self.exptime
            ttime = exptime +0.32*(1-gexp)
            self.SetExposureTime(ttime)
            
            n = self.n
            self.SetExposures(n,1)
            
            y1 = self.y1
            y2 = self.y2
            
            self.SetRegionOfInterest(1,240,0,319)
            
            self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 1)
            time.sleep(2e-4*n)
            self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 0)
            self.com.trigger(self.bank, 'PROG_CTRL_SR')
            self.com.trigger(self.bank, 'ADC_FIFO_RST' )
            self.com.trigger(self.bank, 'EXPOSURE_START_TRIGGER')    
            
            
            tempdata = self.com.readfromblockpipeout(162, 32, 240*320*4)
            
            data = bytearray(tempdata)
            dtype = np.dtype('B')
            data_new = np.frombuffer(data,dtype)
            #data = np.frombuffer(tempdata)
            
            print('signals ', data_new.sum())
            #print('signals ', tempdata)
            
            #kazma = int.from
            
            last_points.append(data_new)
            #last_points = last_points[-10000:]
            
            #ani = FuncAnimation(plt.gcf(), self.animate(last_20_points), interval=1000)

            #plt.tight_layout()
            #plt.show()
            
            return tempdata
        
    
        
    def ShowData(self):
        
        
        last_20_points =[]
        while 1:
        
            gexp = self.gexp
            self.com.wireindata(self.bank, 'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE', 1-gexp)
            
            exptime = self.exptime
            ttime = exptime +0.32*(1-gexp)
            self.SetExposureTime(ttime)
            
            n = self.n
            self.SetExposures(n,1)
            
            y1 = self.y1
            y2 = self.y2
            
            self.SetRegionOfInterest(1,240,0,319)
            
            self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 1)
            time.sleep(2e-4*n)
            self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 0)
            self.com.trigger(self.bank, 'PROG_CTRL_SR')
            self.com.trigger(self.bank, 'ADC_FIFO_RST' )
            self.com.trigger(self.bank, 'EXPOSURE_START_TRIGGER')    
            
            
            tempdata = self.com.readfromblockpipeout(162, 32, 240*10*4)
            
            data = bytearray(tempdata)
            dtype = np.dtype('B')
            data_new = np.frombuffer(data,dtype)
            #data = np.frombuffer(tempdata)
            
            print('signals ', data_new.sum())
            #print('signals ', tempdata)
            
            #kazma = int.from_bytes(data,"big")
            
            last_20_points.append(data_new.sum())
            last_20_points = last_20_points[-10000:]
            
            ani = FuncAnimation(plt.gcf(), self.animate(last_20_points), interval=1000)

            plt.tight_layout()
            plt.show()
            
            



    def animate(i, data):
        
            y1 = data
    
        
            plt.cla()
        
            plt.plot(y1, label='Channel 1')
            #plt.plot(y2, label='Channel 2')
        
            plt.legend(loc='upper left')
            plt.tight_layout()       
            
    
        
    def RecordData(self, bitplanes, blocks, file_name):
        
        #blocks = self.blocks
        #blocks =3
        gexp = self.gexp
        
        self.SetExposures(int(blocks*bitplanes + 2*(1-gexp)), 1)
        
        y1 = self.y1
        y2 = self.y2
        
        yrange = (y2-y1) + 1
        
        self.SetRegionOfInterest(y1, y2, 0,319)
        
        self.com.wireindata(self.bank, 'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE', 1-gexp)
        
        exptime = self.exptime
        ttime = exptime + 0.32*(1-gexp)
        
        self.SetExposureTime(ttime)
        
        frames = bitplanes
        
        self.com.trigger(self.bank, 'ADC_FIFO_RST' )
        self.com.trigger(self.bank, 'EXPOSURE_START_TRIGGER')
        
        recording_data = np.zeros((blocks, 3)) # first frame doesnt include anythin so we remove
        
        for ti in range(1, blocks+1):
            
            block_start_time = int(datetime.now().strftime('%H%M%S%f'))
            #t = time.time()
            #print('frames: ', frames)
            
            if ti == 1:
                tempdata = self.com.readfromblockpipeout(163, 128, yrange*10*4*(frames+2*(1-gexp)))
                block_end_time = int(datetime.now().strftime('%H%M%S%f'))
                #tempdata = [ tempdata]
                file = open(file_name+'_block_'+str(ti)+'.bin', "w+b")
                file.write(bytearray(tempdata))
                file.close()
                #recording = np.unpackbits(tempdata_array, axis=0)
                #recording_matrix = recording.reshape((frames+2*(1-gexp), -1))
                #traces = np.sum(recording_matrix, axis = 1)
                #tempdata = self.com.readfromblockpipeout(163, 128, yrange*10*(frames+2*(ti==1)*(1-gexp)*4))
                #recording_data[ti-1, 0]=ti
                #recording_data[ti-1,1] = block_start_time
                #recording_data[ti-1,2] = block_end_time
                #recording_data[ti-1,3:] = traces[-frames:]
            else:
                tempdata = self.com.readfromblockpipeout(163, 128, yrange*10*4*frames)
                block_end_time = int(datetime.now().strftime('%H%M%S%f')) 
                
                #tempdata = [ti, tempdata]
                file = open(file_name+'_block_'+str(ti)+'.bin', "w+b")
                file.write(bytearray(tempdata))
                file.close()
                #tempdata_array = np.asarray(tempdata)
                #recording = np.unpackbits(tempdata_array, axis=0)
                #recording_matrix = recording.reshape((frames, -1))
                #traces = np.sum(recording_matrix, axis = 1)
                #tempdata = self.com.readfromblockpipeout(163, 128, yrange*10*(frames+2*(ti==1)*(1-gexp)*4))
                #block_end_time = int(datetime.now().strftime('%H%M%S%f'))                
                #recording_data[ti-1, 0]=ti
                #recording_data[ti-1,1] = block_start_time
                #recording_data[ti-1,2] = block_end_time
                #recording_data[ti-1,3:] = traces
            #file = open(file_name, "w+b")
            #file.write(bytearray(tempdata))
            #file.close()
            
            #print('recorded time ', time.time()-t)
            # print('imaging data ', tempdata)
            #print('kazma')
            recording_data[ti-1,0]=ti
            recording_data[ti-1,1]=block_start_time
            recording_data[ti-1,2]=block_end_time
            print('block start time : ', block_start_time)
            print('block end time : ', block_end_time)

        np.savetxt(file_name+'_timing_'+'.csv', recording_data, delimiter=",")
        return recording_data
            
        
        
        
        
    def SetTimeGateInput(self, bin_, input_, offset_sel):
        
        
        self.ConnectCheck()
        ltp = bin_.lower()
        
        if ltp == 'bin a':
            tp = 'a'
        elif ltp == 'bin b':
            tp = 'b'
        else:
            print(' * ERROR: Time gate Bin variable must equal Bin A or Bin B.')
            return 
            
        lst = input_.lower()
        
        if lst == 'pulsegen':
            lst_sel = 0
            ip_sel = 0
            os_sel = 0
            
        elif lst == 'optclk':
            lt_sel =1
            ip_sel = 0
            
            loff = offset_sel.lower()
        
            if loff == 'low':
                os_se = 0
            elif loff == 'high':
                os_sel = 1
            else:
                print(' * ERROR: Offset_Sel variable must equal High or Low.')
                return
        elif lst == 'extclk':
            lt_sel = 0
            ip_sel = 1
            os_sel = 0
        else:
            print( '* ERROR: Input variable must equal PulseGen, OptClk or ExtClk.')
            return
        
        
        
        #Bin A
        if tp == 'a':
            
            
            
            if lst == 'pulsegen':
                print(' * Bin A Time Gate set to External Clock through Pulse Gen.')
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_DELAYGEN_LT_SEL',0 )
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_INPUTSEL',0 )
                self.BinAInputSel = 'PulseGen'
                
            elif lst == 'optclk':
                print(' * Bin A Time Gate set to Optical Clock through Pulse Gen.')
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_DELAYGEN_LT_SEL',1 )
                self.BinAInputSel = 'OptClk'
                
                if os_sel:
                    print(' * Optical Clock offset set high.')
                    self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_DELAYGEN_OFFSET_SEL',1) 
                else:
                    print(' * Optical Clock offset set low.')
                    self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_DELAYGEN_OFFSET_SEL',0)
            
            else:
                print(' * Bin A Time Gate set to External Clock. Pulse Gen is bypassed.')
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_INPUTSEL',1)
                self.BinAInputSel = 'ExtClk'
                
                
        #Bin B
        else:
             
            if lst == 'pulsegen':
                print(' * Bin B Time Gate set to External Clock through Pulse Gen.')
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_DELAYGEN_LT_SEL',0)
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_INPUTSEL',0)
                self.BinBInputSel = 'PulseGen'
            elif lst == 'optclk':
                print(' * Bin B Time Gate set to Optical Clock through Pulse Gen.')
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_DELAYGEN_LT_SEL',1)
                self.BinBInputSel = 'OptClk'
                if os_sel:
                    print(' * Optical Clock offset set high.')
                    self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_DELAYGEN_OFFSET_SEL',1)
                else:
                    print(' * Optical Clock offset set low.')
                    self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_DELAYGEN_OFFSET_SEL',0)
            else:
                print(' * Bin B Time Gate set to External Clock. Pulse Gen is bypassed.')
                self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_INPUTSEL',1)
                self.BinBInputSel = 'ExtClk'
            
        
        self.com.trigger(self.bank, 'PROG_CTRL_SR')
                
                
    
    def SensorReset(self):
        
        self.ConnectCheck()
        
        self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 1)
        self.com.wireindata(self.bank, 'SPCIMAGER_CHIP_RESET', 0)
        
        print('* INFO: Sensor Reset - MATLAB Status will not match Sensor Status ')
        
        self.SensorMode = 'Idle'
        
        
        
    def SensorDisconnect(self):
        
        if self.SensorStatus == 'Disconnected':
            print('***WARNING: Sensor already disconnected!')
            return
        
        self.SensorSwitchOffVoltages(0.01)
        
        print('* Disconnected from Sensor')
        
        self.SensorStatus = 'Disconnected'
        
        self.SensorMode = 'Off'
        
        
        
        
    def SetSensorRevision(self, SensorRev_in):
        
        SensorRev_in_lower = SensorRev_in.lower()
        
        set_ = 1
        
        if SensorRev_in_lower == 'spcimager_aa':
            SensorRev = 'SPCIMAGER_AA'
            set_ = 1
        elif SensorRev_in_lower == 'spcimager_ab':
            SensorRev = 'SPCIMAGER_AB'
            set_ = 0
        elif SensorRev_in_lower == 'tacimager_aa':
            SensorRev = 'TACIMAGER_AA'
            set_ = 0
        else:
            print('Sensor Revision Not Recognised!')
            
            
        self.SensorRevision = SensorRev
        
        
        self.com.wireindata(self.bank, 'SPCIMAGER_AA_TRUE_FALSE', set_)
        print('* Sensor Revision-' , SensorRev, 'is selected by Python')
        
        
        
        
        
    def SensorCalibrateResetLevel(self, imgs):
        
        oldVS = self.VS
        oldVG = self.VG
        oldExpTime = self.ExposureTime
        self.SetVoltage('VS', 0.2)
        self.SetVoltage('VG', 0)
        
        self.SetExposureTime(0)
        print('* Capturing reset levels')
        self.ExposureMode(8)
        
        
        
        
        for img in range(1, imgs+1):
            
            if img == 1:
                cumImg = self.CaptureImage
            else:
                cumImg = cumImg + self.CaptureImage
                
        cumImg =np.asarray(cumImg)/np.asarray(imgs)
        self.FPNCorrection = cumImg - 8192
        
        print('* Finished capture. Reset levels saved in object.FPNCorrection')
        
        self.SetExposureMode(0)
        self.SetVoltage('VS', oldVS)
        self.SetVoltage('VG', oldVG)
        self.SetExposureTime(oldExpTime)
        
        
        
        
    def SetSensorMode(self, status):
        
        
        if status == 'Off' or status=='Idle' or status=='Single Shot' or status=='Continuous': 
            self.SensorMode = status
        else:
            print('***ERROR: Sensor status not must be Off, Idle, Single Shot, or Streaming')
        
        
        
        returnMode = self.SensorMode
        
        
    def SetGlobalReset(self, status_in):
        
        status = status_in.lower()
        
        if status == 'off':
            self.com.wireindata(self.bank, 'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE',0)
            print('* Global reset for analogue exposures is off')
            self.GlobalReset = 'Off'
            
        elif status == 'on':
            self.com.wireindata(self.bank, 'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE',1)
            print('* Global reset for analogue exposures is on')
            self.GlobalReset = 'On'
        else:
            print('*** ERROR: GlobalReset must be ON or OFF')
            
    
    
    def SetResetTime(self, rolling_reset_time, global_reset_time):
         
        if rolling_reset_time<16:
            rolling_reset_time_set = 16
            print('*Info: Minimum CDS RST Timing is 16.')
        else:
            rolling_reset_time_set = rolling_reset_time
        
        if global_reset_time<3:
            print('*Info: Minimum Global RST Timing is 3.')
            global_reset_time_set = 3
        else:
            global_reset_time_set = global_reset_time
        
        self.RollingResetTime = rolling_reset_time_set
        self.GlobalResetTime = global_reset_time_set
        
        self.com.wireindata(self.bank, 'ROLLING_RESET_CYCLES', rolling_reset_time_set)
        self.com.wireindata(self.bank, 'GLOBAL_RESET_CYCLES', global_reset_time_set)
        print('Reset times are set')     
    
    
    
    def SetCDSTime(self, cds_time):
        
        if cds_time < 16:
            cds_time_set = 16
            print('* Info: Minimum CDS Timing is 16')
        else:
            cds_time_set = cds_time
            
        self.CDSTime = cds_time_set
        
        self.com.wireindata(self.bank, 'CDS_BLK_AND_SIG_CYCLES',cds_time_set)
        print(' * CDS Blk and Sig times are set.')
        
        
        
        
    def SetColumnScanOutTime(self, ColumnScanOutTime_in, ADC_Signal_Sample_Start_in, ADC_Crowbar_Sample_Start_in):
        
        if(ColumnScanOutTime_in <= 30):
            ColumnScanOutTime_set = 30
        else:
            ColumnScanOutTime_set = ColumnScanOutTime_in
            
            
                
        if(ADC_Signal_Sample_Start_in <= 7):
            ADC_Signal_Sample_Start_set = 3
        else:
            ADC_Signal_Sample_Start_set = ADC_Signal_Sample_Start_in


                
        if(ADC_Crowbar_Sample_Start_in <= 15):
            ADC_Crowbar_Sample_Start_set = 15
        else:
            ADC_Crowbar_Sample_Start_set = ADC_Crowbar_Sample_Start_in
                                
        self.ColumnScanOutTime = ColumnScanOutTime_set
        self.ADC_Signal_Sample_Start = ADC_Signal_Sample_Start_set
        self.ADC_Crowbar_Sample_Start = ADC_Crowbar_Sample_Start_set
                
        self.com.wireindata(self.bank,'COLUMN_CYCLES_CROWBAR',self.ColumnScanOutTime)
        self.com.wireindata(self.bank,'ADC_SIGNALS_START',self.ADC_Signal_Sample_Start)
        self.com.wireindata(self.bank,'ADC_CROWBAR_SAMPLE_START',self.ADC_Crowbar_Sample_Start)
        print(' * Column scan out times are set.')
        


    def SetDigitalTOFAmbientRejection(self, status):
        
        if status == 'on':
            self.DigitalTOFAmbientRejection = 'On'
            self.com.wireindata(self.bank, 'DIGITAL_TOF_AMBIENT_REJECTION_ENABLE',1)
            print(' * Digital TOF Ambient Rejection Enabled.')
        elif status == 'off':
            self.DigitalTOFAmbientRejection = 'Off'
            self.com.wireindata(self.bank, 'DIGITAL_TOF_AMBIENT_REJECTION_ENABLE',0)
            print(' * Digital TOF Ambient Rejection Disabled.')
        else:
            print(' * Error: Digital TOF Ambient Rejection status must be on or off.')
        
    
    def SetVoltage(self, voltageName_in, voltageValue):
         
            self.ConnectCheck()
        
            voltageName = voltageName_in.upper()
        
            if voltageName == 'DAC5':
                self.DAC5 = voltageValue
            elif voltageName == 'DAC6':
                self.DAC6 = voltageValue
            elif voltageName == 'VDDE':
                self.VDDE = voltageValue
            elif voltageName == 'V1V2':
                self.V1V2 = voltageValue
            elif voltageName == 'V3V3':
                self.V3V3 = voltageValue
            elif voltageName == 'VDDOPAMP':
                self.VDDOPAMP = voltageValue
            elif voltageName == 'V3V6':
                self.V3V6 = voltageValue
            elif voltageName == 'V2V7':
                self.V2V7 = voltageValue
            elif voltageName == 'VHV':
                self.VHV = voltageValue
            elif voltageName == 'VHV2':
                self.VHV2 = voltageValue
            elif voltageName == 'VG':
                self.VG = voltageValue
            elif voltageName == 'VS':
                self.VS = voltageValue
            elif voltageName == 'VQ':
                self.VQ = voltageValue
            elif voltageName == 'VREF':
                self.VREF = voltageValue
            elif voltageName == 'IBIAS1':
                self.IBIAS1 = voltageValue
            elif voltageName == 'IBIAS2':
                self.IBIAS2 = voltageValue
            elif voltageName == 'ADCPWR':
                self.ADCPWR = voltageValue
            else:
                print('No voltage with that name exist. Check Input')
         
            voltageSet = 0
            
            if voltageName == 'VHV':
                voltageSet = int(voltageValue*(1000/7.4))
            elif voltageName == 'VHV2':
                voltageSet = int(voltageValue*(1000/7.4))
            else:
                voltageSet = int(voltageValue*(1000))
                
                
                
            self.com.wireindata(self.bank, voltageName, voltageSet)
            
            self.com.progDAC(self.bank, 'ProgResetDAC')
            
            return voltageSet
    
    
    def SetRegionOfInterest(self, RowMin, RowMax, ColMin, ColMax):
        
        if (RowMin>RowMax) or (ColMin>ColMax):
            print('***Error: Region of interest must be set as RowMin, RowMax, ColMin, ColMax.')
            print('***ROI kept at previous values')
            return
        self.RowMin = RowMin
        self.RowMax = RowMax
        
        self.ColMin = ColMin
        self.ColMax = ColMax
        
        self.com.wireindata(self.bank, 'ROI_FIRST_ROW', RowMin)
        self.com.wireindata(self.bank, 'ROI_FIRST_COL', ColMin)
        self.com.wireindata(self.bank, 'ROI_LAST_ROW', RowMax)
        self.com.wireindata(self.bank, 'ROI_LAST_COL', ColMax)
        
        
     
        
        
        
        
    def SetExposures(self, NoOfExposures, PixelBit):
        
        self.com.wireindata(self.bank, 'NO_OF_EXPOSURES', NoOfExposures)
        self.com.wireindata(self.bank, 'DIGITAL_READOUT_PIXEL_BIT', PixelBit)
        self.PixelBit = PixelBit
        self.NoOfExposures = NoOfExposures
        
        
        
        
        
        
        
    def SetExposureTime(self, timeInMicroSecs):
        
        if self.ExposureMode == 3 or self.ExposureMode ==6:
            clockfreq = self.DigClockFreq
            
        else:
            clockfreq = self.ClockFreq
        
        periodInMicroSecs = 1e6*(1/clockfreq)
        
        minExposure = 0 
        maxExposure = (2**32)-20
        
        inputTimeCode = round(timeInMicroSecs/periodInMicroSecs)
        
        if inputTimeCode < minExposure:
            
            inputTimeCode = minExposure
            
            print('*WARNING: Min Exposure is 1 clock cycle. 0 clock Cycles',
                  'sets exposure wih time gate disabled')
        elif inputTimeCode>maxExposure:
            
            inputTimeCode = maxExposure
            
            print('*WARNING: Max Exposure exceeded.')
        
        
        inputTimeCode_LSB = int(655350)&int(inputTimeCode)
        self.com.wireindata(self.bank, 'EXPOSURE_TIME_LSB', inputTimeCode_LSB)
        inputTimeCode_MSB = int(inputTimeCode>>16)
        self.com.wireindata(self.bank, 'EXPOSURE_TIME_MSB', inputTimeCode_MSB)
        
        #it would be good to check error here(we will write it later)
        
        SPI_EXP_TIME = inputTimeCode
        ActualExposureTime = (inputTimeCode)*periodInMicroSecs
        
        self.ExposureTime = ActualExposureTime
                
        return    ActualExposureTime, SPI_EXP_TIME 

    



    def SetExposureMode(self, Mode):
        
        self.ExposureMode = Mode
        
        
        self.com.wireindata(self.bank, 'EXPOSURE_MODE', Mode)
        
        if Mode == 7 or Mode == 6 or Mode == 3:
            
            self.OutputMode = 'Digital'
            
        else:
            
            self.OutputMode = 'Analogue'
            
        print('* Mode set to ', Mode , ' - ', self.OutputMode ,'Readout Mode')
        
        
        
    def SetCrowbar(self, Status):
        
        if Status.lower() == 'on':
            self.Crowbar = 'On'
            self.com.wireindata(self.bank, 'CDS_CROWBAR_DISABLE',0)
            
        else:
            self.Crowbar = 'Off'
            self.com.wireindata(self.bank, 'CDS_CROWBAR_DISABLE',1)
            
            
    def SetLED(self, number):
        self.com.wireindata(self.bank, 'OK_LEDs', number)
        
    def SetPulseGen(self, BinAPos1, BinAPos2, BinADAC, BinBPos1, BinBPos2, BinBDAC):
        
        self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_DELAYGEN_POS1', BinAPos1)
        self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_DELAYGEN_POS2', BinAPos2)
        self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_DELAYGEN_POS1', BinBPos1)
        self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_DELAYGEN_POS2', BinBPos2)
        self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINA_DELAYGEN_DAC', BinADAC)
        self.com.wireindata(self.bank, 'SPCIMAGER_SPI_BINB_DELAYGEN_DAC', BinBDAC)
        self.com.trigger(self.bank, 'PROG_CTRL_SR')
        
        
        self.BinAPos1 = BinAPos1
        self.BinAPos2 = BinAPos2
        
        self.BinBPos1 = BinBPos1
        self.BinBPos2 = BinBPos2
        
        self.BinADAC = BinADAC
        self.BinBDAC = BinBDAC
        
        
        ActualExposureTimeA = 0
        ActualExposureTimeB = 0
        
        
        return ActualExposureTimeA, ActualExposureTimeB
    




    def SensorStartUpVoltages(self, pausetime):
        
        print('* Starting Up Power Supplies and Bias Voltages - In Progress')
        
        vhv_hold = 3.6
        
        VDDEfinal = self.VDDE
        VDDOPAMPfinal = self.VDDOPAMP
        VREFfinal = self.VREF
        V1V2final = self.V1V2
        V3V3final = self.V3V3
        V3V6final = self.V3V6
        V2V7final = self.V2V7
        VHVfinal = self.VHV
        VHV2final = self.VHV2
        
        self.SetVoltage ('ADCPWR', self.ADCPWR)
        
        VGfinal = self.VG;
        VSfinal = self.VS;
        VQfinal = self.VQ;
        
        if VHVfinal > VHV2final:
            VHVmax = VHVfinal
        else:
            VHVmax = VHV2final
            
        if VGfinal >= VSfinal:
            if VGfinal >= VQfinal:
                VBIASmax = VGfinal
            else:
               VBIASmax = VQfinal
        else:
            if VSfinal >= VQfinal:
               VBIASmax = VSfinal
            else:
               VBIASmax = VQfinal
               
               
        self.SetVoltage ('VDDE', 0)
        
        self.SetVoltage ('V1V2', 0)
        
        
        self.SetVoltage ('V3V3', 0)
        
        self.SetVoltage ('V3V6', 0)
		
        self.SetVoltage ('V2V7', 0)
		
        self.SetVoltage ('VHV', 0)
		
        self.SetVoltage ('VHV2', 0)
		
        self.SetVoltage ('VQ', 0)
		
        self.SetVoltage ('VS', 0)
		
        self.SetVoltage ('VG', 0)
		
        self.SetVoltage ('VREF', 0)
		
        self.SetVoltage ('VDDOPAMP', 0)
        
        
        
        for mv in range(0, int(vhv_hold*10)+1):
            vhv_cur = mv/10
            self.SetVoltage('VHV', vhv_cur)
            self.SetVoltage('VHV2', vhv_cur)
            time.sleep(pausetime)
            
            
        for mv in range(0,37):
            v_int = mv / 10
            
            if v_int <= V1V2final:
                self.SetVoltage ('V1V2',v_int)
                
            if v_int <= V3V3final:
                self.SetVoltage ('V3V3',v_int)
                
            if v_int <= V2V7final:
                self.SetVoltage ('V2V7',v_int)
            
            if v_int <= V3V6final:
                self.SetVoltage ('V3V6',v_int)
                
            if v_int <= VDDOPAMPfinal:
                self.SetVoltage ('VDDOPAMP',v_int)
                
            time.sleep(pausetime)
            
        for mv in range(0, int(VDDEfinal*10)+1):
            v_int = mv / 10
            self.SetVoltage('VDDE', v_int)
            time.sleep(pausetime)
            
            
        for mv in range(0, int(VBIASmax*10)+1):
            v_int = mv / 10
            
            if v_int <= VQfinal:
                self.SetVoltage ('VQ',v_int)
            
            if v_int <= VSfinal:
               self.SetVoltage ('VS',v_int)
               
            if v_int <= VGfinal:
                self.SetVoltage ('VG',v_int)
                
                
        self.SetVoltage('VREF', VREFfinal)
        self.SetVoltage('IBIAS2',self.IBIAS2)
        self.SetVoltage('IBIAS1',self.IBIAS1)
        
        
        for mv in range(int(10*vhv_hold), int(10*VHVmax)+1):
            v_int = mv/10
            
            if v_int <= VHVfinal:
               self.SetVoltage ('VHV',v_int) 
             
            if v_int <= VHV2final:
                self.SetVoltage('VHV2', v_int)
            
            time.sleep(pausetime)
            
        
        print(' * Starting Up Power Supplies and Bias Voltages - Complete')
        
    
    
    def SensorSwitchOffVoltages(self, pausetime):
        
        print('* Switching Off Power Supplies and Bias Voltages - In Progress')
        
        vhv_hold = 3.6
        
        
         #Get Sensor current values to ramp from.
		
        VDDEcur = self.VDDE
        
        V1V2cur = self.V1V2
        V3V3cur = self.V3V3
        V3V6cur = self.V3V6
        V2V7cur = self.V2V7
        VHVcur = self.VHV
        VHV2cur = self.VHV2

        #Bias Voltages
        VGcur = self.VG
        VScur = self.VS
        VQcur = self.VQ
            
        
        #ADC Off
        self.SetVoltage ('ADCPWR', 0)
        
		
        #5 - Vq,Vs,Vg
		
        self.SetVoltage ('VQ', 0)
		
        self.SetVoltage ('VS', 0)
		
        self.SetVoltage ('VG', 0)
        
        
        
        if VHVcur > vhv_hold:
            for v_int in np.arange(VHVcur, vhv_hold+0.1, 0.1):
			     
                # if (v_int <= VHV1final): 
				        
                    self.SetVoltage ('VHV',v_int)
                    time.sleep(pausetime)
                    
                    
        if(VHV2cur > vhv_hold):
		     
            for v_int in np.arange( VHV2cur, vhv_hold + 0.1, 0.1):
			     
                # if (v_int <= VHV2final): 
				    
                    self.SetVoltage ('VHV2',v_int)
                    time.sleep(pausetime)
                
        
        #3 - VDDE
		
        self.SetVoltage ('VDDE',0)
		
		#2 - Internal Voltages
        
        self.SetVoltage ('VREF', 0)
		
        self.SetVoltage ('VDDOPAMP', 0)
		
        self.SetVoltage ('V3V3', 0)
		
        self.SetVoltage ('V3V6', 0)
		
        self.SetVoltage ('V2V7', 0)
		
        self.SetVoltage ('V1V2', 0)
        
        self.SetVoltage('IBIAS2',0)
        self.SetVoltage('IBIAS1',0)
		
		#1 - Ramp Down VHV
		
        self.SetVoltage ('VHV',0)
		
        self.SetVoltage ('VHV2',0)
        
        print(' * Switching On Power Supplies and Bias Voltages - Complete')
                    
                    
                    

            
    
    def CheckOpen(self):
        
        print(self.fp.IsOpen())
