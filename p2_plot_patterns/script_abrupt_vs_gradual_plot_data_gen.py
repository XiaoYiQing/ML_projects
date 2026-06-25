


import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt



def line_segment(x_start : int, y_start : int, x_end : int, y_end : int, num_points : int = 100):
    '''
    Simple function to provide the data of a line function between two
    specified points.
    '''

    x = np.linspace(x_start, x_end, num_points)
    # y = m x + b, with m and b from the two points
    m = (y_end - y_start) / (x_end - x_start)
    b = y_start - m * x_start
    y = m * x + b
    return x, y


# x from 0 to 9
x_arr = np.arange(20)           
y_arr = x_arr.copy()            

plt.plot( x_arr, y_arr )
plt.xlabel("x")
plt.ylabel("y")
plt.title("y = x")
plt.grid(True)
plt.show()


# For the smooth descent case, you can use the following function.
# y_min + (y_max - y_min) / (1.0 + np.exp(k * (x - x0)))

# Define the defining properties of the graph.
x_min = 0           # The starting x of the plot.
x_max = 100         # The ending x of the plot.
y_max = 10.0        # The ceiling of y values.
y_min = 1.0         # The floor of y values.


x_drop_start = 25   # x value from where the drop begins.
x_drop_stop = 40    # x value from where the drop cease.

y_drop_start = 9.5  # y value from where the drop begins.
y_drop_end = 1.5    # y value from where the drop cease.


# Segment before drop.
line_len = x_drop_start - x_min + 1
seg1_x_arr, seg1_y_arr = \
    line_segment( x_min, y_max, x_drop_start, y_drop_start, line_len )

# Segment during drop.
line_len = x_drop_stop - x_drop_start + 1
seg2_x_arr, seg2_y_arr = \
    line_segment( x_drop_start, y_drop_start, x_drop_stop, y_drop_end, line_len )

# Segment after drop.
line_len = x_max - x_drop_stop + 1
seg3_x_arr, seg3_y_arr = \
    line_segment( x_drop_stop, y_drop_end, x_max, y_min, line_len )




