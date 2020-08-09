import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy import signal
from scipy.fft import fft, ifft, fftfreq
import seaborn

def main(in_directory):
    seaborn.set()
    data = pd.read_csv(in_directory)
    Freq = 100 #the Hz
    T = 1/Freq
    L= int(data.shape[0])

    #give columns variable names
    x = data['gFx']
    y = data['gFy']
    z = data['gFz']
    total = data['TgF'] 

    # Fourier transforming
    x_fft = fft(x.values)
    X_PSD_o = abs(x_fft)
    freq = fftfreq(L,d = T)
    i = freq>0

    #plting unfiltered data
    plt.subplot(1,2,1)
    plt.plot(freq[i],X_PSD_o[i])
    plt.title("Fourier transform on raw Data")
    plt.xlim(0,20)

    #fourier with butterworth filter on x
    plt.subplot(1,2,2)
    b, a = signal.butter(3, 0.038, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    filtered_x_fft = fft(filtered_x)
    filtered_X_PSD_o = abs(filtered_x_fft)
    filtered_freq = fftfreq(L,d = T)
    filtered_i = freq>0
    #plting filtered data
    plt.subplot(1,2,2)
    plt.plot(filtered_freq[i],filtered_X_PSD_o[i])
    plt.xlim(0,10)
    plt.title("Fourier transform on Butterworth filtered Data")
    plt.show()



    

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)