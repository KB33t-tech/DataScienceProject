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
    Freq = time.count() / time.max() #the Hz can be calculated this way
    T = 1/Freq # T is the period
    L= int(data.shape[0])

    #butter fractions
    strin_but= 2/Freq
    good_but = 10/Freq
    lax_but =  20/Freq
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
    plt.subplot(2,3,1)
    plt.plot(freq[i],X_PSD_o[i])

    #fourier with butterworth filter on x
    # adjust Butter filter until we get 1 peak with minimal effect on power spectral density 

    b, a = signal.butter(3, strin_but, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    filtered_x_fft = fft(filtered_x)
    filtered_X_PSD_o = abs(filtered_x_fft)
    filtered_freq = fftfreq(L,d = T)
    plt.plot(filtered_freq[i],filtered_X_PSD_o[i])
    plt.legend(labels=('raw data','filtered'))
    plt.ylabel("Power Spectral Density")
    plt.title("Fourier transform with critical frequency of %.3f" %strin_but)
    plt.xlabel("Frequency in Hz")
    plt.xlim(0,20)

    #plt scatter below
    plt.subplot(2,3,4)
    plt.plot(time,x,'b.')
    plt.plot(time,filtered_x,'r-')
    plt.ylabel('acceleration in gs (1g ~= 9.8m/s^2)')
    plt.xlabel('time in seconds')
    plt.legend(labels=('raw','filtered'))
    plt.xlim(500,503)

    #plting filtered just right
    plt.subplot(2,3,2)
    plt.xlim(0,20)
    plt.plot(freq[i],X_PSD_o[i])
    b, a = signal.butter(3, good_but, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    filtered_x_fft = fft(filtered_x)
    filtered_X_PSD_o = abs(filtered_x_fft)
    filtered_freq = fftfreq(L,d = T)
    plt.plot(filtered_freq[i],filtered_X_PSD_o[i])
    plt.legend(labels=('raw data','filtered'))
    plt.xlabel("Frequency in Hz")
    plt.ylabel("Power Spectral Density")
    plt.title("Fourier transform with critical frequency of %.2f" %good_but)

    #plt scatter below
    plt.subplot(2,3,5)
    plt.plot(time,x,'b.')
    plt.plot(time,filtered_x,'r-')
    plt.ylabel('acceleration in gs (1g ~= 9.8m/s^2)')
    plt.xlabel('time in seconds')
    plt.legend(labels=('raw','filtered'))
    plt.xlim(500,503)

    #plting filtered data with not enough stringency
    plt.subplot(2,3,3)
    plt.xlim(0,20)
    plt.plot(freq[i],X_PSD_o[i])
    b, a = signal.butter(3, lax_but, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    filtered_x_fft = fft(filtered_x)
    filtered_X_PSD_o = abs(filtered_x_fft)
    filtered_freq = fftfreq(L,d = T)
    plt.plot(filtered_freq[i],filtered_X_PSD_o[i])
    plt.legend(labels=('raw data','filtered'))
    plt.xlabel("Frequency in Hz")
    plt.ylabel("Power Spectral Density")
    plt.title("Fourier transform with critical frequency of %0.2f" %lax_but)

    #plt scatter below
    plt.subplot(2,3,6)
    plt.plot(time,x,'b.')
    plt.plot(time,filtered_x,'r-')
    plt.xlim(500,503)
    plt.savefig('Report_and_Figures/fourier_analysis.png')
    plt.show()
  

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)