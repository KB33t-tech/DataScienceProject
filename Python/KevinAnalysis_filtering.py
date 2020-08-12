import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy import signal
from scipy.fft import fft, ifft
import seaborn

#this is a script to visualize the 3 axis' and total g forces at given time point with 4 subplots
def main(in_directory):
    xrange = 00,205
    yrange = -2.2,3.2

    seaborn.set()
    walking_data = pd.read_csv(in_directory)
    # going to be plotting 4 graphs using 4 different forces
    plt.xlim(xrange)
    plt.subplot(2, 2, 1)
    #without filtering get this:
    plt.plot(walking_data['time'],walking_data['gFx'],'b-',label="without filtering")   
    #applying butterworth, found .02 works best for my settings
    #something interesting to note is that this filter wont work with sams phone
    b, a = signal.butter(4, 0.1, btype='lowpass', analog=False)
    low_passed_x = signal.filtfilt(b, a, walking_data['gFx'])
    plt.plot(walking_data['time'],low_passed_x,'r-',label="with filtering")
    plt.xlabel('time in seconds')
    plt.ylabel('g force in x')
    plt.title('g force in x over time')
    plt.legend(loc='upper right')
    plt.xlim(xrange)
    plt.ylim(yrange)


    #another interesting thing is difference between iphone and android csv formating
    #calls it 'TgF' in android but gFTotal in Iphone

    #y values
    plt.subplot(2, 2, 2)
    plt.plot(walking_data['time'],walking_data['gFy'],'b-',label='without filtering')   
    b, a = signal.butter(4, 0.1, btype='lowpass', analog=False)
    low_passed_y = signal.filtfilt(b, a, walking_data['gFy'])
    plt.plot(walking_data['time'],low_passed_y,'r-',label='with filtering')
    plt.xlabel('time in seconds')
    plt.ylabel('g force in y')
    plt.title('g force in y over time')
    plt.legend(loc='lower right')
    plt.xlim(xrange)
    plt.ylim(yrange)

    # zvalues
    plt.subplot(2, 2, 3)
    plt.plot(walking_data['time'],walking_data['gFz'],'b-',label='without filtering')   
    b, a = signal.butter(4, 0.1, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, walking_data['gFz'])
    plt.plot(walking_data['time'],low_passed,'r-',label='with filtering')
    plt.xlabel('time in seconds')
    plt.ylabel('g force in z')
    plt.title('g force in z over time')
    plt.legend(loc='upper right')
    plt.xlim(xrange)
    plt.ylim(yrange)
    
    
    # total g force
    plt.subplot(2, 2, 4)
    plt.plot(walking_data['time'],walking_data['TgF'],'b-',label='without filtering')   
    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, walking_data['TgF'])
    plt.plot(walking_data['time'],low_passed,'r-',label='with filtering')
    plt.xlabel('time in seconds')
    plt.ylabel('Total g force')
    plt.title('Total g force over time')
    plt.xlim(xrange)
    plt.legend(loc='upper right')
    plt.ylim(yrange)
    figure = plt.gcf()
    figure.set_size_inches(8, 6)
    figure.tight_layout()
    plt.savefig('Report_and_Figures/filtering_analysis.png',dpi=100)
    plt.show()

    # print(walking_data)




if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)