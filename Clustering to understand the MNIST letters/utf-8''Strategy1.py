
# coding: utf-8

# In[1]:


from Precode import *
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
import seaborn as sns; sns.set()
data = np.load('AllSamples.npy')


def initialize_centroids(points, k):
    """returns k centroids from the initial points"""
    centroids = points.copy()
    #np.random.shuffle(centroids)
    return centroids[:k]


def closest_centroid(points, centroids):
    """returns an array containing the index to the nearest centroid for each point"""
    distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
    return np.argmin(distances, axis=0)

def move_centroids(points, closest, centroids):
    """returns the new centroids assigned from the points closest to them"""
    return np.array([points[closest==k].mean(axis=0) for k in range(centroids.shape[0])])

def recalculate_clusters(points, centroids, k):
    """ Recalculates the clusters """
    # Initiate empty clusters
    clusters = {}
    # Set the range for value of k (number of centroids)
    for i in range(k):
        clusters[i] = []
    for data in points:
        euc_dist = []
        for j in range(k):
            euc_dist.append(np.linalg.norm(data - centroids[j]))
        # Append the cluster of data to the dictionary
        clusters[euc_dist.index(min(euc_dist))].append(data)
    return clusters

def x_location(centroids, k):
    """Finding the loss function for the given K"""
    clusters = {}
    clusters = recalculate_clusters(data, move_centroids(data, closest_centroid(data, c), c), k)
    p = []
    loss_func = 0.00
    x_loc = 0.00
    for l in range(3):
        if l in clusters:
            p =  clusters[l]
            for m in p:
                loss_func=loss_func+(np.linalg.norm((p[l] - centroids[l])**2))
       
        x_loc=x_loc+loss_func
    return x_loc
    


# In[2]:


k1,i_point1,k2,i_point2 = initial_S1('6477') # please replace 0111 with your last four digit of your ID


# In[3]:


print(k1)
print(i_point1)
print(k2)
print(i_point2)
k=4  #Keep changing the K to check the cost

print('Initial Centroid data')
print(initialize_centroids(data,k))
c = initialize_centroids(data,k)
closest_centroid(data, c)
centroids=move_centroids(data, closest_centroid(data, c), c)
recalculate_clusters(data, move_centroids(data, closest_centroid(data, c), c), k)


print('Final Centroids:')
print (centroids)
print('Cost:')
print (x_location(centroids, k))

plt.subplot(121)
plt.scatter(data[:, 0], data[:, 1])
centroids = initialize_centroids(data,k)
plt.scatter(centroids[:, 0], centroids[:, 1], c='r', s=100)
plt.show()

plt.subplot(122)
plt.scatter(data[:, 0], data[:, 1])
closest = closest_centroid(data, centroids)
centroids = move_centroids(data, closest_centroid(data, c), c)
plt.scatter(centroids[:, 0], centroids[:, 1], c='r', s=100)


        
        

