import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy import signal
from scipy.fft import fft, ifft

def main(in_directory):
    
    walking_data = pd.read_csv(in_directory)
    #without filtering get this:
    plt.plot(walking_data['time'],walking_data['TgF'],'b.')
    
    #applying butterworth, found .02 works best for my settings
    #something interesting to note is that this filter wont work with sams phone
    plt.subplot(1, 2, 1)
    b, a = signal.butter(3, 0.02, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, walking_data['TgF'])
    plt.plot(walking_data['time'],low_passed,'r.')
    #another interesting thing is difference between iphone and android csv formating
    #calls it 'TgF' in android but gFTotal in Iphone

    #now going to make sub plot with Fourier transformed butterworth
    plt.subplot(1, 2, 2)
    fouriered = fft(low_passed)
    plt.plot(walking_data['time'],fouriered,'g.')
    
    plt.show()

    print(walking_data)

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)