# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 08:46:42 2022

@author: erik.mueller
"""

import numpy as np
from scipy.fft import fft, fftfreq
import scipy.signal
import matplotlib.pyplot as plt

data = np.genfromtxt('../../data/1khznew1.csv', delimiter=',', skip_header=1, skip_footer=1)

x = data[1:]  # extracting all time values
y = data[0:]  # all amplitude value

x = x[:, 0]
y = y[:, 1]

N = len(y)  # getting length of y vector
T = x[-1] - x[0]

# %%
# sample spacing
T = abs((x[0]-x[1]))  # defining Period length
f = (1/T)/1e6
# yf = fft(y) # fft only from y signal 

w = scipy.signal.windows.hann(N)  # hanning window with N samples
ywf = fft(y*w)                    # fft of signal multiplied with hanning window
xf = fftfreq(N, T)[:N//2]         # getting x-values for fft plot

plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-b')

# plotting FFT signal
plt.semilogy(988, 0.0089, 'xr')   # plotting mark at maximum
plt.legend(['FFT', '1kHz Peak'])  # legend
plt.grid()                        # grid
plt.xlim(0, 20000)                # limiting window
plt.xlabel("Frequency in Hz")     # labeling x axis
plt.ylabel("Amplitude in dB")     # labeling y axis
plt.show()                        # show plot
