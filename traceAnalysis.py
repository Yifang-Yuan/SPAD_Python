# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 11:12:47 2021

@author: Yifang
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import FastICA
from scipy import signal
import SPADdemod
import photometry_functions as fp

'''Set basic parameter'''
def Set_filename (dpath, csv_filename="traceValue.csv"):
    #dpath=set_dpath()
    filename = os.path.join(dpath, csv_filename) #csv file is the file contain values for each frame
    return filename
    
def Read_trace (filename,mode="SPAD",dtype="numpy"):
    '''mode can be SPAD or photometry'''
    '''dtype can be numpy or pandas---in the future'''
    if mode =="SPAD":
        trace = np.genfromtxt(filename, delimiter=',')
        return trace
    elif mode =="photometry":
        Two_traces=pd.read_csv(filename)
        Green=Two_traces['Analog1']
        Red=Two_traces[' Analog2']
        return Green,Red

def get_bin_trace (trace,bin_window=10,color='tab:blue'):
    '''Basic filter and smooth'''
    trace = trace.astype(np.float64)
    '''reverse the trace (voltron and ASAP3 is reversed)''' 
    # trace_reverse=np.negative(trace_raw)
    # plot_trace(trace_reverse, name='raw_trace_reverse')     
    trace_binned=np.array(trace).reshape(-1, bin_window).mean(axis=1)
    fig, ax = plt.subplots(figsize=(10,2))
    ax=plot_trace(trace_binned,ax, fs=9938.4/bin_window,color=color,label="Trace_binned to_"+str(int(10000/bin_window))+"Hz")
    ax.set_xlabel('Time(second)')
    ax.set_ylabel('Photon Count')
    return trace_binned

def get_detrend (trace):
    trace_detrend= signal.detrend(trace) 
    fig, ax = plt.subplots(figsize=(15, 3))
    ax=plot_trace(trace_detrend,ax, title="Trace_detrend")
    return trace_detrend

def butter_filter(data, btype='low', cutoff=10, fs=9938.4, order=5):
#def butter_filter(data, btype='high', cutoff=3, fs=130, order=5): # for photometry data  
    # cutoff and fs in Hz
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype=btype, analog=False)
    y = signal.filtfilt(b, a, data, axis=0)
    # fig, ax = plt.subplots(figsize=(15, 3))
    # ax=plot_trace(y,ax, label="trace_10Hz_low_pass")
    return y

'''Use python Scipy to plot PSD'''
def PSD_plot (data,fs=9938.4,method="welch",color='tab:blue',linewidth=1):
    '''Three methods to plot PSD: welch,periodogram,plotlib'''
    fig=plt.figure()
    if method == "welch":
        f, Pxx_den = signal.welch(data, fs=fs, nperseg=4096)       
        plt.semilogy(f, Pxx_den,linewidth=linewidth)
        #plt.ylim([0.5e-3, 1])
        plt.xlabel('frequency [Hz]')
        plt.ylabel('PSD [V**2/Hz]')
    elif method == "periodogram":
        f, Pxx_den = signal.periodogram(data, fs=fs)
        plt.semilogy(f, Pxx_den,linewidth=linewidth)
    elif method == "plotlib":
        plt.psd(data,Fs=fs,linewidth=linewidth)
    return fig

def combineTraces (dpath,fileNum):
    for i in range(fileNum):
        filename = os.path.join(dpath, "traceValue"+str(i+1)+".csv")  #csv file is the file contain values for each frame
        print(filename)
        if i==0:
            trace_raw = np.genfromtxt(filename, delimiter=',')
        else:
            trace_add = np.genfromtxt(filename, delimiter=',')
            trace_raw=np.hstack((trace_raw,trace_add))
    filename = os.path.join(dpath, "traceValueAll.csv")
    np.savetxt(filename, trace_raw, delimiter=",")
    return trace_raw

def getSignal_subtract_freq(trace,fc_g=1000,fc_r=2000,fs=9938.4):
    #Red,Green= SPADdemod.DemodFreqShift (trace,fc_g=fc_g,fc_r=fc_r,fs=9938.4)
    Red,Green= SPADdemod.DemodFreqShift_bandpass (trace,fc_g=fc_g,fc_r=fc_r,fs=9938.4)
    from sklearn import preprocessing
    RedNorm=preprocessing.normalize([Red])
    GreenNorm=preprocessing.normalize([Green])
    Signal=GreenNorm-RedNorm
    return Signal[0]

def getSignal_subtract(Red,Green,fs=9938.4):
    from sklearn import preprocessing
    RedNorm=preprocessing.normalize([Red])
    GreenNorm=preprocessing.normalize([Green])
    Signal=GreenNorm-RedNorm
    return Signal[0]

def getICA (Red,Green):
    channel1=Green
    channel2=Red
    X = np.c_[channel1,channel2]
    # Compute ICA
    ica = FastICA(n_components=2)
    S = ica.fit_transform(X)  # Reconstruct signals
    A = ica.mixing_  # Get estimated mixing matrix
    '''Plot ICA'''
    plt.figure()
    models = [X, S]
    names = [
        "Observations (mixed signal)",
        "ICA recovered signals",
    ]
    colors = ["green", "red"]
    
    for ii, (model, name) in enumerate(zip(models, names), 1):
        plt.subplot(2, 1, ii)
        plt.title(name)
        for sig, color in zip(model.T, colors):
            plt.plot(sig, color=color,alpha=0.5)
    plt.tight_layout()
    plt.show()
    '''get two separated signals'''
    signal1=S[:,0]
    signal2=S[:,1]
    
    return signal1, signal2

'''PSD analysis after subtracting mean'''
def plot_PSD_bands (trace,fs=9938.4):
    from numpy.fft import fft
    t = np.arange(len(trace)) / fs
    
    x = trace                               # Relabel the data variable
    dt = t[1] - t[0]                      # Define the sampling interval
    N = x.shape[0]                        # Define the total number of data points
    T = N * dt                            # Define the total duration of the data
    
    xf = fft(x - x.mean())                # Compute Fourier transform of x
    Sxx = 2 * dt ** 2 / T * (xf * xf.conj())  # Compute spectrum
    Sxx = Sxx[:int(len(x) / 2)]           # Ignore negative frequencies
    
    df = 1 / T.max()                      # Determine frequency resolution
    fNQ = 1 / dt / 2                      # Determine Nyquist frequency
    faxis = np.arange(0,fNQ,df)              # Construct frequency axis

    fig, ax = plt.subplots(2,2,sharey=True)
    
    ax[0,0].plot(faxis, Sxx.real)                 # Plot spectrum vs frequency
    ax[0,0].set_xlim([0, 250])
    #ax[0,0].set_ylim([0, 2])                    # Select frequency range
    ax[0,0].set_title("Wide band",fontsize=8)
    ax[0,0].xaxis.set_tick_params(labelsize=8)
    ax[0,0].yaxis.set_tick_params(labelsize=8)
    
    ax[0,1].plot(faxis, Sxx.real)                 # Plot spectrum vs frequency
    ax[0,1].set_xlim([1, 28])
    #ax[0,1].set_ylim([0, 2])                    # Select frequency range
    ax[0,1].set_title("Theta band",fontsize=8)
    ax[0,1].xaxis.set_tick_params(labelsize=8)
    ax[0,1].yaxis.set_tick_params(labelsize=8)
    
    ax[1,0].plot(faxis, Sxx.real)                 # Plot spectrum vs frequency
    ax[1,0].set_xlim([30, 80])
    #ax[1,0].set_ylim([0, 2])                    # Select frequency range
    ax[1,0].set_title("Gamma band",fontsize=8)
    ax[1,0].xaxis.set_tick_params(labelsize=8)
    ax[1,0].yaxis.set_tick_params(labelsize=8)
    
    ax[1,1].plot(faxis, Sxx.real)                 # Plot spectrum vs frequency
    ax[1,1].set_xlim([100, 220])
    #ax[1,1].set_ylim([0, 2])                    # Select frequency range
    ax[1,1].set_title("Ripple band",fontsize=8)
    ax[1,1].xaxis.set_tick_params(labelsize=8)
    ax[1,1].yaxis.set_tick_params(labelsize=8)
    
    '''How to add a common label'''
    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Frequency [Hz]",fontsize=8)
    plt.ylabel("Power [$\mu V^2$/Hz]",fontsize=8)
    
    fig.tight_layout()
    
    return fig

def plot_PSD_bands_full (trace,fs=9938.4):
    from numpy.fft import fft
    t = np.arange(len(trace)) / fs
    
    x = trace                               # Relabel the data variable
    dt = t[1] - t[0]                      # Define the sampling interval
    N = x.shape[0]                        # Define the total number of data points
    T = N * dt                            # Define the total duration of the data
    
    xf = fft(x - x.mean())                # Compute Fourier transform of x
    Sxx = 2 * dt ** 2 / T * (xf * xf.conj())  # Compute spectrum
    Sxx = Sxx[:int(len(x) / 2)]           # Ignore negative frequencies
    
    df = 1 / T.max()                      # Determine frequency resolution
    fNQ = 1 / dt / 2                      # Determine Nyquist frequency
    faxis = np.arange(0,fNQ,df)              # Construct frequency axis

    fig, ax = plt.subplots(1,1)
    
    ax.plot(faxis, Sxx.real)                 # Plot spectrum vs frequency
    ax.set_xlim([0,5000])
    #ax.set_ylim([0, 1e-7])                    # Select frequency range
    ax.set_title("Full band",fontsize=8)
    ax.xaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_tick_params(labelsize=8)
    return fig
    
def plot_trace(trace,ax, fs=9938.4, label="trace",color='tab:blue'):
    t=(len(trace)) / fs
    taxis = np.arange(len(trace)) / fs
    ax.plot(taxis,trace,linewidth=0.5,label=label,color=color)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim(0,t)
    ax.legend(loc="upper right", frameon=False)
    ax.set_xlabel('Time(second)')
    ax.set_ylabel('Photon Count')
    return ax

def plotSingleTrace (ax, signal, SamplingRate,color='blue'):
    ax.plot(signal,color,linewidth=1,alpha=0.3)
    ax.set_xticklabels(map(int, ax.get_xticks()/SamplingRate),fontsize=20)
    ax.set_yticklabels(ax.get_yticks(),fontsize=20)
    ax.set_xlabel("seconds",fontsize=20)
    return ax 

def photometry_smooth_plot (raw_reference,raw_signal,sampling_rate=500, smooth_win = 10):
    smooth_reference = fp.smooth_signal(raw_reference, smooth_win)
    smooth_signal = fp.smooth_signal(raw_signal, smooth_win)
    
    lambd = 10e8 # Adjust lambda to get the best fit
    porder = 1
    itermax = 15
    
    r_base=fp.airPLS(smooth_reference.T,lambda_=lambd,porder=porder,itermax=itermax)
    s_base=fp.airPLS(smooth_signal,lambda_=lambd,porder=porder,itermax=itermax)
    
    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(211)
    ax1 = fp.plotSingleTrace (ax1, smooth_signal, SamplingRate=sampling_rate,color='blue',Label='smoothed_signal')
    ax1.plot(s_base,'black',linewidth=1)
    ax2 = fig.add_subplot(212)
    ax2 = fp.plotSingleTrace (ax2, smooth_reference, SamplingRate=sampling_rate,color='purple',Label='smoothed_reference')
    ax2.plot(r_base,'black',linewidth=1)
    
    remove=0
    reference = (smooth_reference[remove:] - r_base[remove:])
    signal = (smooth_signal[remove:] - s_base[remove:])  
    
    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(211)
    ax1 = fp.plotSingleTrace (ax1, signal, SamplingRate=sampling_rate,color='blue',Label='corrected_signal')
    
    ax2 = fig.add_subplot(212)
    ax2 = fp.plotSingleTrace (ax2, reference, SamplingRate=sampling_rate,color='purple',Label='corrected_reference')
    
    z_reference = (reference - np.median(reference)) / np.std(reference)
    z_signal = (signal - np.median(signal)) / np.std(signal)
    
    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(211)
    ax1 = fp.plotSingleTrace (ax1, z_signal, SamplingRate=sampling_rate,color='blue',Label='normalised_signal')
    ax2 = fig.add_subplot(212)
    ax2 = fp.plotSingleTrace (ax2, z_reference, SamplingRate=sampling_rate,color='purple',Label='normalised_reference')
    
    from sklearn.linear_model import Lasso
    lin = Lasso(alpha=0.0001,precompute=True,max_iter=1000,
                positive=True, random_state=9999, selection='random')
    n = len(z_reference)
    lin.fit(z_reference.reshape(n,1), z_signal.reshape(n,1))
    z_reference_fitted = lin.predict(z_reference.reshape(n,1)).reshape(n,)
    
    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(111)
    ax1=fp.plotSingleTrace (ax1, z_signal, SamplingRate=sampling_rate,color='blue')
    ax1=fp.plotSingleTrace (ax1, z_reference_fitted, SamplingRate=sampling_rate,color='purple')
    #ax1.plot(z_signal,'blue',linewidth=1)
    #ax1.plot(z_reference_fitted,'purple',linewidth=1)
    
    zdFF = (z_signal - z_reference_fitted)
    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(111)
    ax1=fp.plotSingleTrace (ax1, zdFF, SamplingRate=sampling_rate,color='black',Label='zscore_signal')
    #ax1.plot(zdFF,'black',linewidth=1)
    
    return z_signal
