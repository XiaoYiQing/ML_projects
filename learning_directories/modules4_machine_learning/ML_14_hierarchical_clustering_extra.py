


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs



# Generate random data with 4 variables and 3 main clusters.
X, _ = make_blobs(n_samples=20, centers=3, n_features=4)

# Generate dataframe using the data clusters with four variable names.
df = pd.DataFrame(X, columns=['Feat_1', 'Feat_2', 'Feat_3', 'Feat_4'])

# kmeans = KMeans(n_clusters=3)
# y = kmeans.fit_predict(df[['Feat_1', 'Feat_2', 'Feat_3', 'Feat_4']])


hierarchical_cluster = AgglomerativeClustering(n_clusters=3, \
    metric='euclidean', linkage='ward')
y = hierarchical_cluster.fit_predict(df[['Feat_1', 'Feat_2', 'Feat_3', 'Feat_4']])

df['Cluster'] = y

#print(df.head())
print(df)