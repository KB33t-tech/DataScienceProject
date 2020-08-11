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
    x_acceleration = x_acceleration[x_acceleration['acceleration']>0]
    plt.plot(x_acceleration['time'],x_acceleration['acceleration'])
    plt.show()

    #do some integration to get velocity
    x = x_acceleration
    start = x['time'].min()
    Velocity = integrate.cumtrapz(x_acceleration['acceleration'],x_acceleration['time'],initial=start) #issue here is previous acceleration is added to last
    v = np.cumsum(x_acceleration['acceleration'])
    print(v)
    x['velocity'] = Velocity
    x['velocity'] = x['velocity']-x['velocity'].shift(periods=1) #seeing if possibly issue with cummilitive integration
    x = x[x['velocity']>0]
    plt.plot(x['time'],x['velocity'],'b-')
    plt.show()

    #doing distance

    Dist = np.cumsum(x['velocity'])
    plt.plot(x['time'],Dist,'b.')
    plt.show()

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)