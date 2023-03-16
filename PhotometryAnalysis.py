# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 16:13:41 2022

@author: Yifang
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import photometry_functions as fp

# Folder with your files
folder = 'C:/SPAD/pyPhotometry_v0.3.1/data/' # Modify it depending on where your file is located
#folder ='C:/SPAD/SPADData/JinghuaSampleData/'
# File name
file_name = '1593744R-2023-03-16-142458.csv'   # Change to your data file
# Read the file
df = pd.read_csv(folder+file_name,index_col=False) # Adjust this line depending on your data file
sampling_rate=130
raw_reference = df[' Analog2'][1:]
raw_signal = df['Analog1'][1:]
#%%
fig = plt.figure(figsize=(16, 10))
ax1 = fig.add_subplot(211)
ax1 = fp.plotSingleTrace (ax1, raw_signal, SamplingRate=sampling_rate,color='blue',Label='raw_Signal')
ax2 = fig.add_subplot(212)
ax2 = fp.plotSingleTrace (ax2, raw_reference, SamplingRate=sampling_rate,color='purple',Label='raw_Reference')

#%%
smooth_win = 5
smooth_reference,smooth_signal,r_base,s_base = fp.photometry_smooth_plot (raw_reference,
                                                                          raw_signal,sampling_rate=sampling_rate, smooth_win = smooth_win)
#%%
remove=30*130
reference = (smooth_reference[remove:] - r_base[remove:])
signal = (smooth_signal[remove:] - s_base[remove:])  

fig = plt.figure(figsize=(16, 10))
ax1 = fig.add_subplot(211)
ax1 = fp.plotSingleTrace (ax1, signal, SamplingRate=sampling_rate,color='blue',Label='corrected_signal')

ax2 = fig.add_subplot(212)
ax2 = fp.plotSingleTrace (ax2, reference, SamplingRate=sampling_rate,color='purple',Label='corrected_reference')

#%%
z_reference = (reference - np.median(reference)) / np.std(reference)
z_signal = (signal - np.median(signal)) / np.std(signal)

fig = plt.figure(figsize=(16, 10))
ax1 = fig.add_subplot(211)
ax1 = fp.plotSingleTrace (ax1, z_signal, SamplingRate=sampling_rate,color='blue',Label='normalised_signal')
ax2 = fig.add_subplot(212)
ax2 = fp.plotSingleTrace (ax2, z_reference, SamplingRate=sampling_rate,color='purple',Label='normalised_reference')

#%%
from sklearn.linear_model import Lasso
lin = Lasso(alpha=0.0001,precompute=True,max_iter=1000,
            positive=True, random_state=9999, selection='random')
n = len(z_reference)
lin.fit(z_reference.reshape(n,1), z_signal.reshape(n,1))
z_reference_fitted = lin.predict(z_reference.reshape(n,1)).reshape(n,)

fig = plt.figure(figsize=(16, 5))
ax1 = fig.add_subplot(111)
ax1 = fp.plotSingleTrace (ax1, z_signal, SamplingRate=sampling_rate,color='blue',Label='normalised_signal')
ax1 = fp.plotSingleTrace (ax1, z_reference_fitted, SamplingRate=sampling_rate,color='purple',Label='normalised_signal')

#%%
zdFF = (z_signal - z_reference_fitted)
fig = plt.figure(figsize=(16, 5))
ax1 = fig.add_subplot(111)
ax1 = fp.plotSingleTrace (ax1, zdFF[9880:19890], SamplingRate=sampling_rate,color='black',Label='zscore_signal')
#ax1.set_ylim(-2,5)
#%%
Raw_mean=np.mean(raw_signal)
Raw_Std=np.std(raw_signal)
dffIndex=Raw_Std/Raw_mean
