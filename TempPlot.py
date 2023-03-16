# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 11:11:50 2023

@author: Yifang
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
t = np.linspace(0, 1, 500, endpoint=False)
plt.plot(t, signal.square(2 * np.pi * 5 * t,duty=0.25),color='m')
plt.ylim(-2, 2)

