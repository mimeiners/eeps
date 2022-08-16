# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 14:11:25 2022

@author: erik

from: https://www.codegrepper.com/code-examples/python/python+generate+sine+wave+pyaudio
"""
import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 1.0  # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 10.0   # in seconds, may be float
f =2000.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 
i =1
volume = 0.1
for  i in range (1,10):
	stream.write(volume*samples)
   	volume = volume +0.1

stream.stop_stream()
stream.close()

p.terminate()

#First Volume Percentage: 13% up to 61 dB
# Second up to 41% to 80dB
# third up to 70% up to 100 dB
#fourth up to 100% and 111 dB
