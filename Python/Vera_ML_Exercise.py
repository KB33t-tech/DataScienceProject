import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


# This function reads the csv files and removes uneeded columns
def get_data(filename):
    data = pd.read_csv(filename)
    data = data[['gFx', 'gFy', 'gFz']]
    return data


# This function shows the process of creating labelled data for training and validating
def create_labelled_data():

    walk = get_data('vera_walking.csv')
    jog = get_data('vera_jogging.csv')
    uphill = get_data('vera_uphill.csv')
    stairs = get_data('vera_stairs.csv')
    stand = get_data('vera_standing.csv')

    walk = np.array(walk).reshape(60, 300)
    jog = np.array(jog).reshape(60, 300)
    uphill = np.array(uphill).reshape(15, 300)
    stairs = np.array(stairs).reshape(40, 300)
    stand = np.array(stand).reshape(40, 300)

    walk = pd.DataFrame(data=walk)
    jog = pd.DataFrame(data=jog)
    uphill = pd.DataFrame(data=uphill)
    stairs = pd.DataFrame(data=stairs)
    stand = pd.DataFrame(data=stand)

    walk.insert(0, 'exercise', 'walking')
    jog.insert(0, 'exercise', 'jogging')
    uphill.insert(0, 'exercise', 'uphill')
    stairs.insert(0, 'exercise', 'stairs')
    stand.insert(0, 'exercise', 'standing')

    labelled_df = [walk, jog, uphill, stairs, stand]
    labelled_df = pd.concat(labelled_df)

    labelled_df.to_csv('labelled_exercises.csv', index = False, header = True)


# This function shows the process of creating unlabelled data to be predicted
def create_unlabelled_data():

    walk = get_data('vera_walking2.csv')
    jog = get_data('vera_jogging2.csv')
    uphill = get_data('vera_uphill2.csv')
    stairs = get_data('vera_stairs2.csv')
    stand = get_data('vera_standing2.csv')

    #print(len(walk))
    #print(len(jog))
    #print(len(uphill))
    #print(len(stairs))
    #print(len(stand))

    walk = np.array(walk).reshape(5, 300)
    jog = np.array(jog).reshape(3, 300)
    uphill = np.array(uphill).reshape(3, 300)
    stairs = np.array(stairs).reshape(3, 300)
    stand = np.array(stand).reshape(4, 300)

    walk = pd.DataFrame(data=walk)
    jog = pd.DataFrame(data=jog)
    uphill = pd.DataFrame(data=uphill)
    stairs = pd.DataFrame(data=stairs)
    stand = pd.DataFrame(data=stand)

    walk.insert(0, 'exercise', 'walking')
    jog.insert(0, 'exercise', 'jogging')
    uphill.insert(0, 'exercise', 'uphill')
    stairs.insert(0, 'exercise', 'stairs')
    stand.insert(0, 'exercise', 'standing')

    unlabelled_df = [walk, jog, uphill, stairs, stand]
    unlabelled_df = pd.concat(unlabelled_df)

    unlabelled_df = unlabelled_df.sample(frac=1)

    unlabelled_truth = unlabelled_df[['exercise']]
    unlabelled_truth.to_csv('unlabelled_exercises_truth.csv', index = False, header = True)

    unlabelled_df.loc[:,'exercise'] = 'unknown'
    unlabelled_df.to_csv('unlabelled_exercises.csv', index = False, header = True)


def main(out_directory):

    #create_labelled_data()
    #create_unlabelled_data()

    # labelled data
    data = pd.read_csv(sys.argv[1])
    X = data.iloc[:, 1:]
    y = data['exercise'].values

    # unlabelled data
    unlabelled_data = pd.read_csv(sys.argv[2])
    X_unlabelled_data = unlabelled_data.iloc[:, 1:]

    # train_test_split
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    #model = KNeighborsClassifier(n_neighbors=3)

    flatten_model = make_pipeline(
        PCA(5),
        RandomForestClassifier(n_estimators=150, max_depth=3, min_samples_split=5)
    )

    flatten_model.fit(X_train, y_train)
    print(flatten_model.score(X_train, y_train))
    print(flatten_model.score(X_valid, y_valid))

    predictions = flatten_model.predict(X_unlabelled_data)
    #print(predictions)
    predictions = pd.DataFrame(data = predictions, columns = ['exercise'])
    predictions.to_csv(out_directory + 'prediction_output.csv', index=False)


if __name__ == '__main__':
    out_directory = sys.argv[3]
    main(out_directory)
