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

    #lets try to find velocity
    x_acceleration = pd.DataFrame({'time':time,'g-force':filtered_x})
    x_acceleration['acceleration'] = x_acceleration['g-force'].multiply(9.81)
    x_acceleration = x_acceleration[x_acceleration['acceleration']>2]
    print(x_acceleration['acceleration'].mean())
    plt.plot(x_acceleration['time'],x_acceleration['acceleration'])
    plt.title('+ve acceleration over time')
    plt.xlabel('time(s)')
    plt.ylabel('acceleration m/s$^2$')
    plt.show()

    # #do some integration to get velocity, note that we run into issue of an ever increasing acceleration

    x = x_acceleration
    start = x['time'].min()
    Velocity = integrate.cumtrapz(x_acceleration['acceleration'],x_acceleration['time'],initial=start)

    x['v'] = Velocity
    plt.plot(x['time'],x['v'],'b-')
    plt.show()

    #but realistically I want to see average velocity at a given time so ill do vavg = (vi+1-Vi)/(ti+1-ti)
    x['vi'] = x['v'].shift(periods=1)
    x['ti'] = x['time'].shift(periods=1)
    x['tavg'] =  (x['time']-x['ti'])/2
    x['vavg'] = (x['v']-x['vi'])/(x['time']-x['ti'])
    x['vavg'] = x[x['vavg']>=0]
    plt.plot(x['time'],x['vavg'],'b-')
    plt.show()

    #doing distance
    Dist = np.cumsum(x['vavg'])
    plt.plot(x['time'],Dist,'b.')
    plt.show()
    
    # # we would expect acceleration to actually be zero so will use Mean of a function to adjust things appropriately
    # # will do this by shifting acceleration upwards with constant c which is mean of our
    # c = (x['v'].max()-x['v'].min())/(x['time'].max()-x['time'].min()) 
    # c=2.02
    # x_acceleration['acceleration'] = x_acceleration['acceleration'] + c
    # #now lets see how graph has changed
    # plt.plot(x_acceleration['time'],x_acceleration['acceleration'])
    # plt.xlabel('time(s)')
    # plt.ylabel('acceleration m/s$^2$')
    # plt.show()   
    
    # #lets see if it helps the velocity
    # x = x_acceleration
    # start = x['time'].min()
    # Velocity = integrate.cumtrapz(x_acceleration['acceleration'],x_acceleration['time'],initial=start)

    # x['v'] = Velocity
    # plt.plot(x['time'],x['v'],'b-')
    # # print(x)
    # plt.show()


    # # #doing distance

    # Dist = np.cumsum(x['v'])
    # plt.plot(x['time'],Dist,'b.')
    # plt.show()

    # #playing with grouping Vf and shifting to get a more constant velocity
    # #making new df with just velocity and time
    # vel = pd.DataFrame({"time":x['time'].apply(int),"vf":x['vf']})  #might want to changed apply from int to 

    # grouped = vel.groupby('time')['vf'].mean().reset_index()
    # grouped['vi'] = grouped['vf'].shift(periods=1)
    # grouped['v'] = grouped['vf'] - grouped['vi']
    # plt.plot(grouped.time,grouped.v)
    # plt.show()

    # #distance by grouping
    # Dist = np.cumsum(grouped['v'])
    # plt.plot(grouped['time'],Dist,'b.')
    # plt.show()


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)