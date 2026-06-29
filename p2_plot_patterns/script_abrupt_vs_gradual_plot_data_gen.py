


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


from plot_funcs import Lin3SegmConfig
from plot_funcs import gen_Lin3SegmPlotData


# ======================================================================= >>>>>
#       Linear Function Data Set Gen
# ======================================================================= >>>>>

# The range of mid points allowed.
drop_mid_pt_rng = ( 0.10, 0.90 )
# The range of width the linear drop is allowed.
drop_width_rng = ( 0.02, 0.08 )

# The range of y starting value (highest point)
y_max_rng = ( 0.90, 0.95 )
# The range of y ending value (lowest point)
y_min_rng = ( 0.05, 0.10 )

# The slight dip in y from its highest point to the point where the main drop occurs.
y_pre_drop_dip_rng = ( 0.01, 0.05 )
# The slight dip in y from where the main drop ends to the lowest y value.
y_post_drop_dip_rng = ( 0.01, 0.05 )

# Define the number of random test cases.
n = 100
# Generate the randomized parameters for the three segments linear plot.
drop_mid_pt_arr = np.random.uniform( drop_mid_pt_rng[0], drop_mid_pt_rng[1], size = n )
drop_width_arr = np.random.uniform( drop_width_rng[0], drop_width_rng[1], size = n )
y_max_arr = np.random.uniform( y_max_rng[0], y_max_rng[1], size = n )
y_min_arr = np.random.uniform( y_min_rng[0], y_min_rng[1], size = n )
y_pre_drop_dip_arr = np.random.uniform( y_pre_drop_dip_rng[0], y_pre_drop_dip_rng[1], size = n )
y_post_drop_dip_arr = np.random.uniform( y_post_drop_dip_rng[0], y_post_drop_dip_rng[1], size = n )


for z in range(n):

    myConfig_z = Lin3SegmConfig()
    myConfig_z.x1 = 0
    myConfig_z.y1 = y_max_arr[z]
    myConfig_z.x2 = drop_mid_pt_arr[z] - drop_width_arr[z]/2
    myConfig_z.y2 = y_max_arr[z] - y_pre_drop_dip_arr[z]
    myConfig_z.x3 = drop_mid_pt_arr[z] + drop_width_arr[z]/2
    myConfig_z.y3 = y_min_arr[z] + y_post_drop_dip_arr[z]
    myConfig_z.x4 = 1
    myConfig_z.y4 = y_min_arr[z]
    myConfig_z.data_pt_cnt = 100

    x_arr_z, y_arr_z = gen_Lin3SegmPlotData( myConfig_z )

    plt.plot( x_arr_z, y_arr_z )
    

plt.xlabel("x")
plt.ylabel("y")
plt.title("y = x")
plt.grid(True)
plt.show()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Linear Function Data Set Gen
# ======================================================================= >>>>>



# ======================================================================= <<<<<

# For the gradually steeper drop profile.
# y_min + (y_max - y_min) * np.exp(-k * x)