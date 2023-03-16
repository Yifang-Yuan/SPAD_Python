# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 20:50:05 2022

@author: Yifang
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import traceAnalysis as Ananlysis
import SPADdemod
import SPADreadBin

def getSignalTrace (filename, traceType='Constant',HighFreqRemoval=True,getBinTrace=False,bin_window=20):
    '''TraceType:Freq, Constant, TimeDiv'''
    trace=Ananlysis.Read_trace (filename,mode="SPAD")
    if HighFreqRemoval==True:
            trace=Ananlysis.butter_filter(trace, btype='low', cutoff=2000, fs=9938.4, order=10)  
    if traceType=='Constant':
        if getBinTrace==True:
            trace_binned=Ananlysis.get_bin_trace(trace,bin_window=bin_window,color='m')
            #trace_binned=Ananlysis.get_bin_trace(trace,bin_window=bin_window)
            return trace_binned
        else:
            return trace
    if traceType=='Freq':
        #Red,Green= SPADdemod.DemodFreqShift (trace,fc_g=1000,fc_r=2000,fs=9938.4)
        Red,Green= SPADdemod.DemodFreqShift_bandpass (trace,fc_g=1009,fc_r=1609,fs=9938.4)
        #Red=Ananlysis.butter_filter(Red, btype='low', cutoff=200, fs=9938.4, order=10)
        #Green=Ananlysis.butter_filter(Green, btype='low', cutoff=200, fs=9938.4, order=10)
        Signal=Ananlysis.getSignal_subtract(Red,Green,fs=9938.4)
        return Red,Green,Signal
    if traceType=='TimeDiv': 
        #need to be modified for different time division traces
        lmin,lmax=SPADdemod.hl_envelopes_max(trace, dmin=1, dmax=1, split=True)
        fig, ax = plt.subplots(figsize=(12, 3))
        ax.plot(lmax,trace[lmax], color='g')
        ax.plot(lmin,trace[lmin], color='r')
        x_green, Green=SPADdemod.Interpolate_timeDiv (lmax,trace)
        x_red, Red=SPADdemod.Interpolate_timeDiv (lmin,trace)
        
        Signal=Ananlysis.getSignal_subtract(Red,Green,fs=9938.4)
        fig, ax = plt.subplots(figsize=(12, 3))
        ax=Ananlysis.plot_trace(Signal,ax, label="Signal")    
        return Red,Green,Signal
    
def findMask(trace,high_thd,low_thd=0):
    mask=trace.copy()
    mask[mask>high_thd]=0
    mask[mask<low_thd]=0
    mask[mask!=0]=1
    return mask

def findTraceFromMask(trace,high_thd,low_thd=0):
    mask=findMask(trace,high_thd=high_thd,low_thd=low_thd)
    signal_index=np.where(mask==1)[0]
    x, sig=SPADdemod.Interpolate_timeDiv (signal_index,trace)
    return x,sig
'find opto stimulation'
def find_optoPeak (filename,Height,Distance):
    from scipy.signal import find_peaks
    trace=Ananlysis.Read_trace (filename,mode="SPAD")
    peaks, _ = find_peaks(trace, height=Height, distance=Distance)
    return peaks

def ReadTwoROItrace (dpath):
    filename_g=Ananlysis.Set_filename (dpath,"traceGreenAll.csv")
    filename_r=Ananlysis.Set_filename (dpath,"traceRedAll.csv")
    Green_raw=getSignalTrace (filename_g,traceType='Constant',HighFreqRemoval=False,getBinTrace=False)
    Red_raw=getSignalTrace (filename_r,traceType='Constant',HighFreqRemoval=False,getBinTrace=False)
    fig, ax = plt.subplots(figsize=(12, 2.5))
    Ananlysis.plot_trace(Green_raw[0:200],ax, fs=9938.4, label="Green data trace")
    fig, ax = plt.subplots(figsize=(12, 2.5))
    Ananlysis.plot_trace(Red_raw[0:200],ax, fs=9938.4, label="Red data trace")
    return Green_raw,Red_raw
    
def DemodTwoTraces (Green_raw, Red_raw):
    lmin,lmax=SPADdemod.Find_targetPeaks(Green_raw, dmin=1, dmax=1,high_limit=2200, low_limit=1500)
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(lmax,Green_raw[lmax], color='g')
    #ax.plot(lmin,Green_raw[lmin], color='k')
    x_green, Green=SPADdemod.Interpolate_timeDiv (lmax,Green_raw)
    #x_dark, Dark=SPADdemod.Interpolate_timeDiv (lmin,Green_raw)
    
    lmin,lmax=SPADdemod.Find_targetPeaks(Red_raw, dmin=1, dmax=1,high_limit=1200, low_limit=500)
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(lmax,Red_raw[lmax], color='r')
    #ax.plot(lmin,Red_raw[lmin], color='k')
    x_red, Red=SPADdemod.Interpolate_timeDiv (lmax,Red_raw)
    #x_dark, Dark=SPADdemod.Interpolate_timeDiv (lmin,Red_raw)
    
    return Green, Red
#%%
'''Read files'''
dpath="C:/SPAD/SPADData/20230315/2023_3_15_12_38_28_1629818_r10uWg5uW_turnOffLightInMiddle"
# Sampling Frequency
fs   = 9938.4
'''Read binary files'''
#count_value=readMultipleBinfiles(dpath,9,xxRange=[40,200],yyRange=[60,220])  ##for single ROI
#Green,Red=SPADreadBin.readMultipleBinfiles_twoROIs(dpath,18,xxrange_g=[90,210],yyrange_g=[10,110],xxrange_r=[60,180],yyrange_r=[140,240]) #two ROIs
'''Show images'''
# filename = os.path.join(dpath, "spc_data1.bin")
# Bindata=SPADreadBin(filename,pyGUI=False)
# ShowImage(Bindata,dpath)
'''Count trace values'''
# count_value=countTraceValue(dpath,Bindata,xxrange=[40,200],yyrange=[60,220])  
#%% Two ROIs
Green_raw,Red_raw = ReadTwoROItrace (dpath)
#%%
Green, Red= DemodTwoTraces (Green_raw[0:850000], Red_raw[0:850000])
#%%
Green =Ananlysis.butter_filter(Green_raw, btype='low', cutoff=2000, fs=9938.4, order=10)
Red=Ananlysis.butter_filter(Red_raw, btype='low', cutoff=2000, fs=9938.4, order=10)
#%%
z_signal=Ananlysis.photometry_smooth_plot (Red,Green,sampling_rate=9938.4,smooth_win =100)
#%%
fig, ax = plt.subplots(figsize=(12, 2.5))
Ananlysis.plot_trace(z_signal[50000:150000],ax, fs=9938.4, label="z_score signal")
#%%
nfft = 256  # FFT size
window = np.hamming(nfft)  # Window function
powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(z_signal, Fs=fs)
#%%
from scipy.io import wavfile
plt.pcolormesh(time, freqenciesFound, 10*np.log10(powerSpectrum))  # Convert power to dB
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.ylim(-1, 500)
plt.show()

#%% Single ROIs



filename=Ananlysis.Set_filename (dpath,"traceValue1.csv")
Signal_raw=getSignalTrace (filename,traceType='Constant',HighFreqRemoval=False,getBinTrace=False,bin_window=100)
fig, ax = plt.subplots(figsize=(12, 2.5))
Ananlysis.plot_trace(Signal_raw,ax, fs=9938.4, label="Raw data trace")
#%%
bin_window=100
Tracebinned=Ananlysis.get_bin_trace(Signal_raw,bin_window=bin_window)
#%%
fig, ax = plt.subplots(figsize=(12, 2.5))
Ananlysis.plot_trace(Signal_raw[800000:801000],ax, fs=9938.4, label="Raw data trace")

#%%
Red,Green,Signal=getSignalTrace (filename,traceType='TimeDiv',HighFreqRemoval=False,getBinTrace=False,bin_window=400)
#%%
correct_signal=Ananlysis.photometry_smooth_plot (Red,Green,sampling_rate=9938.4,smooth_win =400)
#%%
bin_window=200
Signal_bin=Ananlysis.get_bin_trace(correct_signal,bin_window=bin_window)

#%% find opto stimulation
x_optoPeak= find_optoPeak (filename,10000,80000)
#%%
fig, ax = plt.subplots(figsize=(5, 5))
transient=np.zeros(20000)
for i in range (0,len(x_optoPeak)):
    #Ananlysis.plotSingleTrace (ax, correct_signal[x_optoPeak[i]:x_optoPeak[i]+9500], SamplingRate=9938.4,color='tab:blue')
    ax.plot(correct_signal[x_optoPeak[i]:x_optoPeak[i]+20000], color="tab:blue",alpha=0.3)
    ax.set_xticklabels(map(float, ax.get_xticks()/10000),fontsize=10)
    ax.set_yticklabels(ax.get_yticks(),fontsize=10)
    ax.set_xlabel("seconds",fontsize=20)
    transient=transient+correct_signal[x_optoPeak[i]:x_optoPeak[i]+20000]
average_transient=transient/len(x_optoPeak)
ax.plot(average_transient, color="k",alpha=1)

#%%
