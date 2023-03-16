#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 18:52:39 2021

@author: kurtulus
"""

import pandas as pd
import numpy as np 
import ok


class SPCIMAGERAA_2021():

    def __init__(self):
        
        df = pd.DataFrame(columns = ['name','addr','size','bit'])
        df.loc[1] = ['OK_LEDs', '00', 8, 0]
        df.loc[2] = ['VHV', '01', 12, 0]
        df.loc[3] = ['VHV2', '02', 12, 0]
        df.loc[4] = ['VS', '03', 12, 0]
        df.loc[5] = ['VG', '04', 12, 0]
        df.loc[6] = ['VQ', '05', 12, 0]
        df.loc[7] = ['VREF', '06', 12, 0]
        df.loc[8] = ['V3V3', '07', 12, 0]
        df.loc[9] = ['V2V7', '08', 12, 0]
        df.loc[10] = ['IBIAS1', '09', 12, 0]
        df.loc[11] = ['IBIAS2', '0a', 12, 0]
        df.loc[12] = ['V3V6', '0b', 12, 0]
        df.loc[13] = ['VDDOPAMP', '0c', 12, 0]
        df.loc[14] = ['VDDE', '0d', 12, 0]
        df.loc[15] = ['V5_SET', '0e', 12, 0]
        df.loc[16] = ['ADCPWR', '0f', 12, 0]
        df.loc[17] = ['V1V2', '10', 12, 0]
        df.loc[18] = ['DAC5', '11', 12, 0]
        df.loc[19] = ['DAC6', '12', 12, 0]
        df.loc[20] = ['ProgResetDAC', '40', 2, 0]
        df.loc[21] = ['ProgResetDAC_Ret', '20', 2, 2]
        df.loc[22] = ['ADC_PU', '20', 1, 4]
        df.loc[23] = ['Mode', '00', 8, 8]
        df.loc[24] = ['FSMState', '20', 8, 5]
        df.loc[25] = ['SPCIMAGER_SPI_BINA_DELAYGEN_POS1', '13', 7, 0]
        df.loc[26] = ['SPCIMAGER_SPI_BINA_DELAYGEN_POS2', '13', 7, 7]
        df.loc[27] = ['SPCIMAGER_SPI_BINA_DELAYGEN_DAC', '14', 4, 0]
        df.loc[28] = ['SPCIMAGER_SPI_BINA_DELAYGEN_LT_SEL', '13', 1, 14]
        df.loc[29] = ['SPCIMAGER_SPI_BINA_DELAYGEN_OFFSET_SEL', '13', 1, 15]
        df.loc[30] = ['SPCIMAGER_SPI_BINB_DELAYGEN_POS1', '15', 7, 0]
        df.loc[31] = ['SPCIMAGER_SPI_BINB_DELAYGEN_POS2', '15', 7, 7]
        df.loc[32] = ['SPCIMAGER_SPI_BINB_DELAYGEN_DAC', '14', 4, 4]
        df.loc[33] = ['SPCIMAGER_SPI_BINB_DELAYGEN_LT_SEL', '15', 1, 14]
        df.loc[34] = ['SPCIMAGER_SPI_BINB_DELAYGEN_OFFSET_SEL', '15', 1, 15]
        df.loc[35] = ['SPCIMAGER_SPI_BINA_OUT_ENABLE', '14', 1, 8]
        df.loc[36] = ['SPCIMAGER_SPI_BINB_OUT_ENABLE', '14', 1, 9]
        df.loc[37] = ['SPCIMAGER_SPI_BINA_INPUTSEL', '14', 1, 10]
        df.loc[38] = ['SPCIMAGER_SPI_BINB_INPUTSEL', '14', 1, 11]
        df.loc[39] = ['ROI_FIRST_ROW', '16', 8, 0]
        df.loc[40] = ['ROI_LAST_ROW', '16', 8, 8]
        df.loc[41] = ['ROI_FIRST_COL', '17', 9, 0]
        df.loc[42] = ['ROI_FIRST_ROW', '18', 9, 0]
        df.loc[43] = ['EXPOSURE_START_TRIGGER', '44', 1, 0]
        df.loc[44] = ['RST_CTRL_SR', '41', 1, 0]
        df.loc[45] = ['PROG_CTRL_SR', '42', 1, 0]
        df.loc[46] = ['PROG_COMPLETE', '60', 1, 0]
        df.loc[47] = ['ADC_FIFO_OUT', 'A2', 16, 0]
        df.loc[48] = ['ADC_FIFO_RST', '43', 1, 0]
        df.loc[49] = ['SPCIMAGER_CHIP_RESET', '14', 1, 12]
        df.loc[50] = ['EXPOSURE_TIME_LSB', '1A', 16, 0]
        df.loc[51] = ['EXPOSURE_TIME_MSB', '1B', 16, 0]
        df.loc[52] = ['EXPOSURE_MODE', '17', 5, 10]
        df.loc[53] = ['EXPOSURE_TIME_LSB_RET', '24', 16, 0]
        df.loc[54] = ['EXPOSURE_TIME_MSB_RET', '25', 16, 0]
        
        df.loc[55] = ['FIFO_WR_COUNT', '22', 16, 0]
        df.loc[56] = ['FIFO_WR_LIMIT', '23', 16, 0]
        df.loc[57] = ['DEBUG_PULSERESET', '45', 1, 0]
        df.loc[58] = ['CDSBLK_DISABLE', '14', 1, 13]
        df.loc[59] = ['CDSSIG_DISABLE', '14', 1, 14]
        df.loc[60] = ['CDS_CROWBAR_DISABLE', '14', 1, 15]
        
        df.loc[61] = ['NO_OF_EXPOSURES', '19', 32, 0]
        df.loc[62] = ['DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE', '18', 1, 11]
        df.loc[63] = ['FIRMWARE_REVISION', '3f', 16, 0]
        df.loc[64] = ['DIGITAL_READOUT_PIXEL_BIT', '18', 1, 10]
        df.loc[65] = ['ROLLING_RESET_CYCLES', '1c', 8, 0]
        df.loc[66] = ['GLOBAL_RESET_CYCLES', '1d', 16, 0]
    
        df.loc[67] = ['COLUMN_CYCLES_CROWBAR', '1e', 8, 0]
        df.loc[68] = ['ADC_SIGNALS_START', '1e', 8, 8]
        df.loc[69] = ['ADC_CROWBAR_SAMPLE_START', '1f', 8, 0]
        df.loc[70] = ['CDS_BLK_AND_SIG_CYCLES', '1f', 8, 8]
        df.loc[71] = ['SPCIMAGER_AA_TRUE_FALSE', '01', 1, 15]
        df.loc[72] = ['SINGLE_BIT_FIFO_OUT', 'A3', 32, 0]
        df.loc[73] = ['DIGITAL_TOF_AMBIENT_REJECTION_ENABLE', '01', 1, 14]
        
        self.bank =df


        

    def progDAC(self, bank, ProgResetDACName):
        
        #reset trigger for DACs
        
        #bank is df here 
        
        length = bank.shape[0]
        
        name = bank['name']
        addr = bank['addr']
        size = bank['size']
        bit = bank['bit']
        
        bankindex = list(name).index(ProgResetDACName)
        address = bank['addr'].iloc[bankindex]
        address = np.uint16(int(address,16))
        
        
        self.dev.ActivateTriggerIn(address,0)
        
    def trigger(self, bank, ProgResetDACName):
        
        length = bank.shape[0]
        
        name = bank['name']
        addr = bank['addr']
        size = bank['size']
        bit = bank['bit']
        
        bankindex = list(name).index(ProgResetDACName)
        address = bank['addr'].iloc[bankindex]
        address = np.uint16(int(address, 16))
        bit = bank['bit'].iloc[bankindex]
        
        self.dev.ActivateTriggerIn(addr, bit)
        
        

    def wireindata(self, df, wirename, data):
        
        
        
        length = df.shape[0]
        
        name = df['name']
        addr = df['addr']
        size = df['size']
        bit = df['bit']
        
        bankindex = list(name).index(wirename)
        banksize = df['size'].iloc[bankindex]
        bit = df['bit'].iloc[bankindex]
        address = df['addr'].iloc[bankindex]
        address = np.uint16(int(address,16))
        
        sz = (2**banksize)-1
        mask = np.uint32(sz<<bit)
        
        d = data<<size
        
        self.dev.SetWireInValue(address, d, mask)
        self.dev.UpdateWireIns()
    

        
        
        
    def readfromblockpipeout(self, epaddr, blksize, bsize, psize):
        
        psize = bsize
        
        buf = bytearray(psize)
        
        return self.dev.ReadFromBlockPipeOut(epaddr, blksize, buf)



   
    
    

    
    
    




















