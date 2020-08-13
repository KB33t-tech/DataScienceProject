import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy import signal
from scipy.fft import fft, ifft, fftfreq
import seaborn
from scipy import integrate



def main(in_directory):
    #loading in data and setting seaborn for any plots 
    data = pd.read_csv(in_directory)
    seaborn.set()

    # print(data)
    #give columns variable names
    time = data['time']
    x = data['gFx']
    print(data)
    # print(x)
    # total = data['']

    #useful values
    Freq = time.count() / time.max() #the Hz can be calculated this way
    good_but = 10/Freq

    # Filtering
    b, a = signal.butter(3, good_but, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)

    #Noticed that if window is too large method wont work so this limits window and correct for
    x_acceleration = pd.DataFrame({'time':time,'g-force':filtered_x})
    x_acceleration = x_acceleration[x_acceleration['time']>488]
    x_acceleration = x_acceleration[x_acceleration['time']<490]
    x_acceleration['acceleration'] = x_acceleration['g-force'].multiply(9.81)
    x_acceleration['acceleration'] = x_acceleration['acceleration']-x_acceleration['acceleration'].mean()

    print(x_acceleration['acceleration'].mean())
    plt.plot(x_acceleration['time'],x_acceleration['acceleration'])


    # # #do some integration to get velocity, note that we run into issue of an ever increasing acceleration

    x = x_acceleration
    start = x['time'].min()

    Velocity = integrate.cumtrapz(x_acceleration['acceleration'],x_acceleration['time'],initial=start)
    
    plt.subplot(1,3,1)
    plt.plot(x_acceleration['time'],x_acceleration['acceleration'],'g-',label='acceleration')
    plt.title('acceleration over time')
    plt.xlabel('time(s)')
    plt.ylabel('acceleration m/s$^2$')
    plt.legend()

    plt.subplot(1,3,2)
    plt.plot(x_acceleration.iloc[1:,0],Velocity[1:],'b-',label='velocity')
    plt.title('velocity over time')
    plt.xlabel('time(s)')
    plt.ylabel('velocity m/s')
    plt.legend()   

    #integrating the distance and plot
    Dist = integrate.cumtrapz(Velocity,x_acceleration['time'],initial=start)
    plt.subplot(1,3,3)
    plt.plot(x_acceleration.iloc[1:,0],Dist[1:],'r-',label='distance') #had to remove first line of plot because of issue with nature of integrals
    plt.title('distance over time')
    plt.xlabel('time(s)')
    plt.ylabel('distance m')
    plt.legend()
    figure = plt.gcf()
    figure.set_size_inches(8, 6)
    figure.tight_layout()
    plt.savefig('Report_and_Figures/vel_dist_short.png',dpi=100)
    plt.show()

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)