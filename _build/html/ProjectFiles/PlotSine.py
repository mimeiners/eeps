#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 07:22:17 2022

@author: erik
"""

import numpy as np
from scipy.signal import butter, lfilter, freqz,find_peaks
import matplotlib.pyplot as plt

figWidth = 16 # Width of many of the figures



sampleFrequency = 32767 # Hz
bandwidth = sampleFrequency / 2 # 0-512 Hz (also Nyquist freq)
sampleDuration = 1.0 / sampleFrequency # time duration per cycle
y = np.random.rand(sampleFrequency)
signalTime = np.arange(0, 1, sampleDuration)
signalFreq = 440 # Hz
signalSamples440 = np.sin(2.0 * np.pi * signalFreq * signalTime)

signalSamples = (signalSamples440 + 5*y)/2 #



plt.figure('Sine Only', figsize=(figWidth,4))
plt.plot(signalTime,signalSamples440)
plt.xlabel("t in s")
plt.ylabel("Amplitude")
plt.suptitle('Source Signal')
plt.xlim(0, 0.0022)
plt.show()

plt.figure('Noisy Source Signal',figsize=(figWidth, 4))
plt.plot(signalTime, signalSamples)
plt.xlabel("t in s")
plt.ylabel("Amplitude")
plt.suptitle('Source Signal')
plt.xlim(0, 0.0044)
plt.show()


# fft of signal
fftFreqs = np.arange(bandwidth)
fftValues = (np.fft.fft(signalSamples) / sampleFrequency)[:int(bandwidth)+1]
fftabs = np.absolute(fftValues)
peak = find_peaks(fftabs, height=(0.01))
height = peak[1]['peak_heights']
peak_pos = fftFreqs[peak[0]]

maximum = np.max(height)
indexplace = np.where(height==maximum)
indexvalue= height[indexplace]

fftmax = np.where(fftabs==maximum)


index_pos = peak_pos[indexplace]

plt.figure('FFT Source')
plt.plot(fftFreqs, np.absolute(fftValues), index_pos,indexvalue,'o','r')
plt.xlim(0, bandwidth)
plt.ylim(0, 0.3)
plt.xlabel("Frequency in Hz")
plt.ylabel("Magnitude")
plt.suptitle("Source Signal Frequency Components")
plt.show()

#%%

def pdm(x):
    n = len(x)
    y = np.zeros(n)
    error = np.zeros(n+1)    
    for i in range(n):
    	y[i] = 1 if x[i] >= error[i] else 0
    error[i+1] = y[i] - x[i] + error[i]
    return y, error[0:n]

n = 100
fclk = 250e6 # clock frequency (Hz)
t = np.arange(n) / fclk
f_sin = 5e6 # sine frequency (Hz)

x = 0.5 + 0.4 * np.sin(2*np.pi*f_sin*t)
y, error = pdm(x)

plt.plot(1e9*t, x, label='input signal')
plt.step(1e9*t, y, label='pdm signal',  linewidth=2.0)
plt.step(1e9*t, error, label='error')
plt.xlabel('Time (ns)')
plt.ylim(-0.05,1.05)
plt.legend()
plt.show()