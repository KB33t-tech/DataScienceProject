import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy import signal
from scipy.fft import fft, ifft, fftfreq
import seaborn
from scipy import integrate
import math
from scipy.special import cbrt


def main(in_directory):
    #loading in data and setting seaborn for any plots 
    data = pd.read_csv(in_directory)
    seaborn.set()

    # #trying to get cubic acceleration with this section of code but could not get it to work
    # axis = data['gFx']*-1 #multiplying by -1 to get right distance
    # axis2 = data['gFy']-1
    # axis3 = data['gFx']*-1
    # cubedsum = (axis**3)+(axis2**3)+(axis3**3)
    # taxis = cbrt(cubedsum)

    time = data['time']
    axis = 'gFx'
    x = data[axis]*-1 #-ves are forward steps

    #useful values for filtering
    Freq = time.count() / time.max() #the Hz can be calculated this way
    good_but = 10/Freq

    # Filtering and putting into pandas
    b, a = signal.butter(3, good_but, btype='lowpass', analog=False)
    filtered_x = signal.filtfilt(b, a, x)
    x_acceleration = pd.DataFrame({'time':time,'g-force':filtered_x})
    x_acceleration['acceleration'] = x_acceleration['g-force'].multiply(9.81)
   
    #this time i need to calculate the rolling integration 
    Section = math.ceil((Freq*1)) #Freq * x , whatever your multiply by Freq is number of seconds we are looking at.
    vel = x_acceleration
    vel = vel.set_index('time')
    vel = vel.rolling(Section).apply(integrate.trapz)

    vel = vel.reset_index()
    vel = vel.dropna()
    vel['velocity'] = vel['acceleration']*(1/(Section)) #dx was 1 but really out dx would be 1/Freq 

    #was curious what removing things not in average would do
    # vel = vel[vel['velocity']>=vel['velocity'].mean()] #remove weird noise possibly due to walking backwards
    
    plt.subplot(1,2,1)
    plt.plot(vel['time'],vel['velocity'],label='Velocity' )
    plt.title('velocity over time')
    plt.xlabel('time(s)')
    plt.ylabel('velocity m/s')
    plt.legend()
       

    #integrating the distance and plot
    start = vel['time'].min() 
    Dist = integrate.cumtrapz(vel['velocity'],vel['time'],initial=start)

    #Plotting and saving figures
    plt.subplot(1,2,1)
    plt.subplot(1,2,2)
    plt.plot(vel['time'],Dist,'r-',label='distance') #had to remove first line of plot because of issue with nature of integrals
    plt.title('distance over time')
    plt.xlabel('time(s)')
    plt.ylabel('distance m')
    plt.legend()
    figure = plt.gcf()
    figure.set_size_inches(8, 6)
    figure.tight_layout()
    figure.savefig('Report_and_Figures/Vel&Dist_'+axis+'.png', dpi=100)
    plt.show()

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)