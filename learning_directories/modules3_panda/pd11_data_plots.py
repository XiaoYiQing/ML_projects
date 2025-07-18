


'''
Plotting
Pandas uses the plot() method to create diagrams.

We can use Pyplot, a submodule of the Matplotlib library to visualize 
the diagram on the screen.

Read more about Matplotlib in our Matplotlib Tutorial.
'''


# ======================================================================= >>>>>
#	Initialization
# ======================================================================= >>>>>

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "pd10_data"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

df = pd.read_csv( dataFile_fullName )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Data Plot: Standard
# ======================================================================= >>>>>

# Plot all data columns on the y-axis with the indexing as the x-axis.
plt.figure(0)
df.plot()
plt.show(block = False)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Data Plot: Scatter
# ======================================================================= >>>>>

'''
Scatter Plot
Specify that you want a scatter plot with the kind argument:
kind = 'scatter'

A scatter plot needs an x- and a y-axis.
In the example below we will use "Duration" for the x-axis and "Calories" 
for the y-axis.
Include the x and y arguments like this:
x = 'Duration', y = 'Calories'
'''

# Scatter plot between 'Duration' and 'Calories'.
plt.figure(1)
df.plot(kind = 'scatter', x = 'Duration', y = 'Calories')
plt.show(block = False)

'''
Remember: In the previous example, we learned that the correlation between 
"Duration" and "Calories" was 0.922721, and we concluded with the fact that 
higher duration means more calories burned.

By looking at the above scatter plot, we can see the association clearly too.
'''

# Scatter plot between 'Duration' and 'Calories'.
plt.figure(2)
df.plot(kind = 'scatter', x = 'Duration', y = 'Maxpulse')
plt.show(block = False)
# A scatterplot where there are no relationship between the columns.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Data Plot: Histogram
# ======================================================================= >>>>>

'''
Use the kind argument to specify that you want a histogram:

kind = 'hist'

A histogram needs only one column.

A histogram shows us the frequency of each interval, e.g. how many workouts 
lasted between 50 and 60 minutes?
'''

# In the example below we will use the "Duration" column to create the histogram:
plt.figure(5)
df["Duration"].plot(kind = 'hist')
plt.xlabel( "Duration" )
plt.show(block = True)
# Note: The histogram tells us that there were over 100 workouts that lasted 
# between 50 and 60 minutes.

# ======================================================================= <<<<<

