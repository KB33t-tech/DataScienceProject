import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


def get_pca(X):
    
    flatten_model = make_pipeline(
        MinMaxScaler(),
        PCA(2)
    )
    X2 = flatten_model.fit_transform(X)
    assert X2.shape == (X.shape[0], 2)
    return X2


def get_clusters(X):

    model = make_pipeline(
        KMeans(n_clusters=5)
    )
    model.fit(X)
    return model.predict(X)


def main():

    # labelled data
    data = pd.read_csv(sys.argv[1])
    X = data.iloc[:, 1:]
    y = data['exercise'].values

    # unlabelled data
    unlabelled_data = pd.read_csv(sys.argv[2])
    X_unlabelled_data = unlabelled_data.iloc[:, 1:]
    #print(X_unlabelled_data)

    # train_test_split
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    #model = KNeighborsClassifier(n_neighbors=3)

    # Random Forest model
    flatten_model = make_pipeline(
        PCA(10),
        RandomForestClassifier(n_estimators=100, max_depth=3, min_samples_split=5)
    )

    flatten_model.fit(X_train, y_train)
    print(flatten_model.score(X_train, y_train))
    print(flatten_model.score(X_valid, y_valid))

    predictions = flatten_model.predict(X_unlabelled_data)
    #print(predictions)
    predictions = pd.DataFrame(data = predictions, columns = ['exercise'])
    predictions.to_csv(sys.argv[3] + 'prediction_output.csv', index=False) # output saved to Raw_data/


    # PCA(2) and KMeans(5) to plot the clusters
    X2 = get_pca(X)
    clusters = get_clusters(X)
    plt.scatter(X2[:, 0], X2[:, 1], c=clusters, cmap='Set1', edgecolor='k', s=20)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Clusters of Similar Exercise Observations')
    plt.show()
    #plt.savefig('Cluster_Exercise')

    df = pd.DataFrame({
        'cluster': clusters,
        'exercise': y,
    })
    counts = pd.crosstab(df['exercise'], df['cluster'])
    print(counts)


if __name__ == '__main__':
    main()
