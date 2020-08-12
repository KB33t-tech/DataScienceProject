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
    # total = data['']

    #useful values
    Freq = time.count() / time.max() #the Hz can be calculated this way
    good_but = 10/Freq

    # Filtering
    b, a = signal.butter(3, good_but, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)

    #lets try to find velocity
    x_acceleration = pd.DataFrame({'time':time,'g-force':filtered_x})
    x_acceleration = x_acceleration[x_acceleration['time']>460]
    x_acceleration = x_acceleration[x_acceleration['time']<480]
    x_acceleration['acceleration'] = x_acceleration['g-force'].multiply(9.81)
    print(x_acceleration)

    print(x_acceleration)
    
    x_acceleration['acceleration'] = x_acceleration['acceleration']-x_acceleration['acceleration'].mean() #x_acceleration['acceleration'].mean()
    x_acceleration['abs'] = x_acceleration['acceleration'].abs()
    # x_acceleration = x_acceleration[x_acceleration['abs']>5]

    print(x_acceleration['acceleration'].mean())
    plt.plot(x_acceleration['time'],x_acceleration['acceleration'])
    plt.title('acceleration over time')
    plt.xlabel('time(s)')
    plt.ylabel('acceleration m/s$^2$')
    plt.show()

    # # #do some integration to get velocity, note that we run into issue of an ever increasing acceleration

    x = x_acceleration
    start = x['time'].min()
    df = pd.DataFrame()
    df['time'] = x['time']
    df['v'] = x_acceleration['acceleration']
    # df['v'] = integrate.cumtrapz(x_acceleration['acceleration'],x_acceleration['time'],initial=start)
    df = df.set_index('time')

    print(df)
    df = df.rolling(window = 100).apply(integrate.trapz)
    print(df)
    Velocity = integrate.cumtrapz(x_acceleration['acceleration'],x_acceleration['time'],initial=start)
    
    print(df)
    # x = x[x['v']>0]
    plt.plot(df.index,df['v'],'b-',label='velocity')
    plt.plot(x_acceleration['time'],x_acceleration['acceleration'],'g-',label='acceleration')
    plt.title('velocity over time')

    Dist = integrate.cumtrapz(Velocity,x_acceleration['time'],initial=start)
    plt.plot(x_acceleration['time'],Dist,'r-',label='distance')
    plt.legend()
    plt.show()




if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)