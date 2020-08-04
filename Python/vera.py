import sys
from pyspark.sql import SparkSession, functions, types
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


def get_data(filename):
    return pd.read_csv(filename)


def main():

    data = pd.read_csv('walk_vera.csv', parse_dates = ['time'])
    data = data[0:3000]

    # noise filtering on gFTotal
    b, a = signal.butter(5, 0.06, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, data['gFTotal'])

    # get ms^2 and velocity
    data['ms2'] = data['gFTotal'] * 9.80665
    data['next_time'] = data['time'].shift(-1)
    data.dropna(subset = ['next_time'], inplace=True)
    data['time_diff'] = (data['next_time'] - data['time']).dt.total_seconds()
    data['velocity'] = data['ms2'] * data['time_diff']
    data['low_passed_gFTotal'] = pd.DataFrame(data=low_passed, columns=['low_passed_gFTotal'])

    print(data)

    corrMatrix = data.corr()
##    plt.matshow(corrMatrix)
##    plt.xticks(range(data.shape[1]-1), ('gFx', 'gFy', 'gFz', 'gFTotal'))
##    plt.yticks(range(data.shape[1]-1), ('gFx', 'gFy', 'gFz', 'gFTotal'))
##    plt.colorbar()
##    plt.savefig('data_corr.png')
    

##    plt.plot(data['gFTotal'], 'b.', alpha = 0.5)
##    plt.plot(data['low_passed_gFTotal'], 'r-', alpha = 0.8)
##    plt.show()


main()
