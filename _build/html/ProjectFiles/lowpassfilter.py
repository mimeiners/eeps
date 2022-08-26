# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 09:52:38 2022

@author: jan.droest
"""

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Setting standard filter requirements.
order = 6
fs = 44000.0       
cutoff = 1000

b, a = butter_lowpass(cutoff, fs, order)

# Plotting the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Creating the data for filteration
T = 5.0         # value taken in seconds
n = int(T * fs) # indicates total samples
t = np.linspace(0, T, n, endpoint=False)

data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Filtering and plotting
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()


#%% PDM code

figWidth = 16 # Width of many of the figures

sampleFrequency = 32767 # Hz
bandwidth = sampleFrequency / 2 # 0-512 Hz (also Nyquist freq)
sampleDuration = 1.0 / sampleFrequency # time duration per cycle

signalTime = np.arange(0, 1, sampleDuration)
signal1Freq = 1000 # Hz
signal1Samples = np.sin(2.0 * np.pi * signal1Freq * signalTime)
signal2Freq = 2000 # Hz
signal2Samples = np.sin(2.0 * np.pi * signal2Freq * signalTime)
signalSamples = (signal1Samples + signal2Samples) / 2


plt.figure(figsize=(figWidth, 4))
plt.plot(signalTime, signalSamples)
plt.xlabel("t")
plt.ylabel("Amplitude")
plt.suptitle('Source Signal')
plt.show()


# fft of signal
fftFreqs = np.arange(bandwidth)
fftValues = (np.fft.fft(signalSamples) / sampleFrequency)[:int(bandwidth)+1]
plt.figure('FFT Source')
plt.plot(fftFreqs, np.absolute(fftValues))
plt.xlim(0, bandwidth)
plt.ylim(0, 0.3)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.suptitle("Source Signal Frequency Components")
plt.show()


#%% pdm freqenz

pdmFreq = 64
pdmPulses = np.empty(sampleFrequency * pdmFreq)
pdmTime = np.arange(0, pdmPulses.size)

pdmIndex = 0
signalIndex = 0
quantizationError = 0
while pdmIndex < pdmPulses.size:
    sample = signalSamples[signalIndex]
    signalIndex += 1
    for tmp in range(pdmFreq):
        if sample >= quantizationError:
            bit = 1
        else:
            bit = -1
        quantizationError = bit - sample + quantizationError
        pdmPulses[pdmIndex] = bit
        pdmIndex += 1

print(pdmIndex, signalIndex, pdmPulses.size, signalSamples.size)

#%% 4k sample 
span = 1024
plt.figure(figsize=(16, 6))
counter = 1
for pos in range(0, pdmIndex, span):
    from matplotlib.ticker import MultipleLocator
    plt.subplot(4, 1, counter)
    counter += 1
    
    # Generate a set of time values that correspond to pulses with +1 values. Remove the rest
    # and plot.
    plt.vlines(np.delete(pdmTime[pos:pos + span], np.nonzero(pdmPulses[pos:pos + span] > 0.0)[0]), 0, 1, 'g')
    plt.ylim(0, 1)
    plt.xlim(pos, pos + span)
    plt.tick_params(axis='both', which='major', labelsize=8)
    ca = plt.gca()
    axes = ca.axes
    axes.yaxis.set_visible(False)
    # axes.yaxis.set_ticklabels([])
    axes.xaxis.set_ticks_position('bottom')
    # axes.xaxis.set_ticks(np.arange(pos, pos + span, 64))
    axes.xaxis.set_major_locator(MultipleLocator(64))
    spines = axes.spines
    for tag in ('top', 'bottom'):
        spines[tag].set_visible(False)
    if counter == 5:
        break
plt.show()

#%% lowpass filtering


# Setting standard filter requirements.
order = 6
fs = 44000.0       
cutoff = 1000

derivedSamples = butter_lowpass_filter(pdmPulses, cutoff, fs, order)

# plots
plt.figure(figsize=(figWidth, 4))
plt.plot(derivedSamples)
plt.xlabel("t")
plt.ylabel("Amplitude")
plt.suptitle('Derived Signal')
plt.show()

fftFreqs = np.arange(bandwidth)
fftValues = (np.fft.fft(derivedSamples) / sampleFrequency)[:int(bandwidth)+1]
plt.figure()
plt.plot(fftFreqs, np.absolute(fftValues))
plt.xlim(0, bandwidth)
plt.ylim(0, 0.3)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.suptitle("Derived Signal Frequency Components")
plt.show()

