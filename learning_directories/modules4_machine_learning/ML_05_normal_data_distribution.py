


'''
In this chapter we will learn how to create an array where the values are concentrated around a given value.

In probability theory this kind of data distribution is known as the normal data distribution, or the Gaussian data distribution, after the mathematician Carl Friedrich Gauss who came up with the formula of this data distribution.
'''


import numpy
import matplotlib.pyplot as plt

# Normal distribution with mean as 5.0 and the standard deviation as 1.0.
x = numpy.random.normal(5.0, 1.0, 30000)

# Draw the histogram with 100 bars.
plt.hist(x, 100)
plt.show()

# The plot shows that the values should be concentrated around 5.0, 
# and rarely further away than 1.0 from the mean.
