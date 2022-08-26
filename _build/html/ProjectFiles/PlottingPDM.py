#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 05:45:15 2022

@author: erik
"""

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from scipy.signal import butter, lfilter, freqz, decimate


def read_datafile(file_name):
    # the skiprows keyword is for heading, but I don't know if trailing lines
    # can be specified
    data = np.loadtxt(file_name, delimiter=',', skiprows=10)
    return data

data = np.genfromtxt('1khznew1.csv', delimiter=',', skip_header=1,
                     skip_footer=1)#, names=['time','value'])

data1 = np.genfromtxt('1kHzMeas_91dB.csv', delimiter=',', skip_header=1,
                     skip_footer=1)#, names=['time','value'])

x = data[1:] #all time
y = data[0:262142]  #all value

x1 = data[0:1024] #all time
y1 = data[1:1025]  #all value

x= x[:,0]
y= y[:,1]

x1= x1[:,0]
y1= y1[:,0]


fig = plt.figure(1)

plt.plot(x,y, color='r', label='the data')

leg = plt.legend('Test')

plt.show()



#%% lowpass filtering

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=6):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

pdmPulses = data[1:,]
pdmPulses = pdmPulses[:,1]
# Setting standard filter requirements.
order = 6
fs = 44000.0       
cutoff = 1000

sampleFrequency = 32764 # Hz
bandwidth = sampleFrequency / 2 # 0-512 Hz (also Nyquist freq)
sampleDuration = 0.001 / sampleFrequency # time duration per cycle

derivedSamples = butter_lowpass_filter(pdmPulses, cutoff, fs, order)
#t = np.linspace(0,0.001, num=16382)
# plots
plt.figure('DerivedSamples')
plt.plot(derivedSamples)
plt.xlabel("t")
plt.ylabel("Amplitude")
plt.suptitle('Derived Signal')
plt.show()

fftFreqs = np.arange(bandwidth)
fftValues = (np.fft.fft(derivedSamples) / sampleFrequency)[:int(bandwidth)]
plt.figure()
plt.plot(fftFreqs, np.absolute(fftValues))
plt.xlim(0, bandwidth)
plt.ylim(0, 0.03)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.suptitle("Derived Signal Frequency Components")
plt.show()
#%%
q=64
n=2
ftype= 'iir'

wave_duration = 1
sample_rate = 44000
freq = 2816000
bandwidth = freq/64
samples_decimated = int(len(pdmPulses)/q)+1

pdmnew = decimate(pdmPulses,q,n,ftype)
xnew = np.linspace(0, wave_duration, samples_decimated, endpoint=False)


plt.figure('DecimatedSignal')
plt.plot(xnew, pdmnew, '.-')
plt.xlabel('Time, Seconds')
plt.legend(['data', 'decimated'], loc='best')
plt.show()

fftFreqs= np.arange(freq/2)
fftValues= (np.fft.fft(pdmnew)/freq)[:int(bandwidth)]

plt.figure('New FFT')
plt.plot(fftFreqs, np.absolute(fftValues))
plt.xlim(0, bandwidth*2)
plt.ylim(0, 0.03)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.suptitle("Derived Signal Frequency Components")
plt.show()