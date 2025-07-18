


'''
Earlier in this tutorial we have worked with very small amounts of data in our examples, just to understand the different concepts.

In the real world, the data sets are much bigger, but it can be difficult to gather real world data, at least at an early stage of a project.

How Can we Get Big Data Sets?
To create big data sets for testing, we use the Python module NumPy, which comes with a number of methods to create random data sets, of any size.
'''


import numpy

# Import the matplotlib.pyplot module under the alias plt.
import matplotlib.pyplot as plt


# ======================================================================= >>>>>
#	Percentiles
# ======================================================================= >>>>>


# Create an array containing 10 random floats between 0 and 5:
x = numpy.random.uniform(0.0, 5.0, 10)
print(x)

# You can create however many entries (under hardware limitation), 
# but we refrain from doingithere to avoid cluttering the command prompt.


# To visualize the data set we can draw a histogram with the data we collected.
# We will use the Python module Matplotlib to draw a histogram.
# Learn about the Matplotlib module in our Matplotlib Tutorial.
x = numpy.random.uniform(0.0, 5.0, 250)

# Draw the histogram with 5 bars
plt.hist(x, 5)
plt.show()
# The first bar represents how many values in the array are between 0 and 1.
# The second bar represents how many values are between 1 and 2.
# Etc.

# ======================================================================= <<<<<





