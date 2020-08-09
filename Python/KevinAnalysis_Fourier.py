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
    time = data['time']
    Freq = time.count() / time.max() #the Hz
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
    plt.subplot(1,3,3)
    plt.plot(freq[i],X_PSD_o[i])

    #fourier with butterworth filter on x
    # adjust Butter filter until we get 1 peak with minimal effect on power spectral density 

    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    filtered_x_fft = fft(filtered_x)
    filtered_X_PSD_o = abs(filtered_x_fft)
    filtered_freq = fftfreq(L,d = T)
    filtered_i = freq>0
    plt.plot(filtered_freq[i],filtered_X_PSD_o[i])
    plt.legend(labels=('raw data','filtered'))
    plt.ylabel("Power Spectral Density")
    plt.title("Fourier transform with critical frequency of 0.1")
    plt.xlabel("Frequency in Hz")
    plt.xlim(0,20)

    #plting filtered data too stringently
    plt.subplot(1,3,1)
    plt.xlim(0,20)
    plt.plot(freq[i],X_PSD_o[i])
    b, a = signal.butter(3, 0.02, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    filtered_x_fft = fft(filtered_x)
    filtered_X_PSD_o = abs(filtered_x_fft)
    filtered_freq = fftfreq(L,d = T)
    filtered_i = freq>0
    plt.plot(filtered_freq[i],filtered_X_PSD_o[i])
    plt.legend(labels=('raw data','filtered'))
    plt.xlabel("Frequency in Hz")
    plt.ylabel("Power Spectral Density")
    plt.title("Fourier transform with critical frequency of 0.02")

    #plting filtered data too stringently
    plt.subplot(1,3,2)
    plt.xlim(0,20)
    plt.plot(freq[i],X_PSD_o[i])
    b, a = signal.butter(3, 0.05, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    filtered_x_fft = fft(filtered_x)
    filtered_X_PSD_o = abs(filtered_x_fft)
    filtered_freq = fftfreq(L,d = T)
    filtered_i = freq>0
    plt.plot(filtered_freq[i],filtered_X_PSD_o[i])
    plt.legend(labels=('raw data','filtered'))
    plt.xlabel("Frequency in Hz")
    plt.ylabel("Power Spectral Density")
    plt.title("Fourier transform with critical frequency of 0.05")


    plt.show()
  

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)