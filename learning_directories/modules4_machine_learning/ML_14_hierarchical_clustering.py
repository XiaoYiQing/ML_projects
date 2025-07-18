

'''
Hierarchical Clustering

Hierarchical clustering is an unsupervised learning method for 
clustering data points. 
The algorithm builds clusters by measuring the dissimilarities between data. 
Unsupervised learning means that a model does not have to be trained, 
and we do not need a "target" variable. 
This method can be used on any data to visualize and interpret the relationship 
between individual data points.

Here we will use hierarchical clustering to group data points and visualize 
the clusters using both a dendrogram and scatter plot.
'''


'''
How does it work?

We will use Agglomerative Clustering, a type of hierarchical clustering 
that follows a bottom up approach. 
We begin by treating each data point as its own cluster. 
Then, we join clusters together that have the shortest distance between 
them to create larger clusters. 
This step is repeated until one large cluster is formed containing all of 
the data points.

Hierarchical clustering requires us to decide on both a distance and linkage 
method. We will use euclidean distance and the Ward linkage method, 
which attempts to minimize the variance between clusters.
'''


# ======================================================================= >>>>>
#	Hierarchical Clustering
# ======================================================================= >>>>>

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.datasets import make_blobs

x = [4, 5, 10, 4, 3, 11, 14 , 6, 10, 12]
y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21]

plt.figure(1)
plt.scatter(x, y)
plt.show(block=False)




# Create a list of grouped items sharing the same indices from each of the
# x and y lists.
data = list( zip(x, y) )
# Now we compute the ward linkage using euclidean distance, 
# and visualize it using a dendrogram:
linkage_data = linkage(data, method='ward', metric='euclidean')

plt.figure(2)
dendrogram(linkage_data)
plt.show(block=False)

'''
On the dendrogram plot, you are to read from bottom to top.

At the bottom level, the x-axis represents the indices of the item group in "data".
For example, we see that indices 2 and 5 are grouped, meanning that the link
is established between the items (10,24) and (11,25).
This linking is indicated by the two vertical lines arising from the x-axis at
the location of indices 2 and 5.
The two lines are connected by a horizontal line at y-axis value of 1.414.
Why at elevation 1.414? 
Because the euclidean distance between (10,24) and (11,25) is sqrt of 2!

On the next level, the item of index 6 (14,24) is grouped with the resulting grouping 
of items of index 2 and 5.
I do not understand exactly how it is calculated, but you gonna have to look up
the user manual for the "linkage" method when the "ward" option is used.
'''

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Hierarchical Clustering (Agglomerative Clustering)
# ======================================================================= >>>>>

# Here, we do the same thing with Python's scikit-learn library. 
# Then, visualize on a 2-dimensional plot.

from sklearn.cluster import AgglomerativeClustering

hierarchical_cluster = AgglomerativeClustering(n_clusters=2, metric='euclidean', linkage='ward')
labels = hierarchical_cluster.fit_predict(data)

plt.figure(3)
plt.scatter(x, y, c=labels)
plt.show()

# ======================================================================= <<<<<



