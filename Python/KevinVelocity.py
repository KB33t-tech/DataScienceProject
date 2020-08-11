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

    #useful values
    Freq = time.count() / time.max() #the Hz can be calculated this way
    good_but = 10/Freq

    # Filtering
    b, a = signal.butter(3, good_but, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    # filtered_x = x #to check unfiltered
    #lets try to find velocity
    x_acceleration = pd.DataFrame({'time':time,'g-force':filtered_x})
    x_acceleration['acceleration'] = x_acceleration['g-force'].multiply(9.81)
    x_acceleration = x_acceleration[x_acceleration['acceleration']>0]
    plt.plot(x_acceleration['time'],x_acceleration['acceleration'])
    plt.show()
    # print(x_acceleration)
    #do some integration to get velocity
    x = x_acceleration
    start = x['time'].min()
    Velocity = integrate.cumtrapz(x_acceleration['acceleration'],x_acceleration['time'],initial=start) #issue here is previous acceleration is added to last

    x['vf'] = Velocity
    x['vi'] = x['vf'].shift(periods=1)
    x['v'] = x['vf'] - x['vi'] #seeing if possibly issue with cummilitive integration
    plt.plot(x['time'],x['v'],'b-')
    # print(x)
    plt.show()

    #doing distance

    Dist = np.cumsum(x['v'])
    plt.plot(x['time'],Dist,'b.')
    plt.show()

    #playing with grouping Vf and shifting to get a more constant velocity
    #making new df with just velocity and time
    vel = pd.DataFrame({"time":x['time'].apply(int),"vf":x['vf']})  #might want to changed apply from int to 

    grouped = vel.groupby('time')['vf'].mean().reset_index()
    grouped['vi'] = grouped['vf'].shift(periods=1)
    grouped['v'] = grouped['vf'] - grouped['vi']
    plt.plot(grouped.time,grouped.v)
    plt.show()

    #distance by grouping
    Dist = np.cumsum(grouped['v'])
    plt.plot(grouped['time'],Dist,'b.')
    plt.show()


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)