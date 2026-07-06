

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


from plot_funcs import gen_linPolyLin_plotData
from plot_funcs import PolyDropFuncConfig

from toolbox.file_nav import next_free_name
from toolbox.file_nav import file_exists



# ======================================================================= >>>>>
#       Randomized Data Set Gen
# ======================================================================= >>>>>

# Define the number of random test cases.
n = 2000

fourPts = np.zeros((4, 2))
fourPts[0][0] = 0.0;  fourPts[0][1] = 1.00
fourPts[1][0] = 0.2;  fourPts[1][1] = 0.98
fourPts[2][0] = 0.8;  fourPts[2][1] = 0.05
fourPts[3][0] = 1.0;  fourPts[3][1] = 0.02

poly_cfig = PolyDropFuncConfig
poly_cfig.z = 4.0
poly_cfig.u_start = 0.2

# Plot starting point.
x0 = 0;     y0 = 1
# Poly drop start point range.
x1_rng = ( 0.01, 0.50 )
y1_rng = ( 0.95, 0.99 )
# Poly drop end point range.
x2_rng = ( 0.30, 0.80 )
y2_rng = ( 0.20, 0.06 )
# End y value range of the trailing linear segment.
y3_rng = ( 0.01, 0.05 )
# Plot final x.
x3 = 1

# Polynomial degree range.
z_rng = ( 1.5, 10 )
# Range of percentage of poly drop portion forced being flat.
u_start_rng = ( 0.05, 0.7 )


# Generate the randomized parameters for the lin-poly-lin plot.
x1_arr = np.random.uniform( x1_rng[0], x1_rng[1], size = n )
y1_arr = np.random.uniform( y1_rng[0], y1_rng[1], size = n )
x2_arr = np.random.uniform( x2_rng[0], x2_rng[1], size = n )
y2_arr = np.random.uniform( y2_rng[0], y2_rng[1], size = n )
y3_arr = np.random.uniform( y3_rng[0], y3_rng[1], size = n )
z_arr = np.random.uniform( z_rng[0], z_rng[1], size = n )
u_start_arr = np.random.uniform( u_start_rng[0], u_start_rng[1], size = n )


# Rearrange x2 points ending up below corresponding x1 points.
a = x2_rng[1] - x2_rng[0]
for z in range(n):
    if x1_arr[z] > x2_arr[z]:
        b = x2_rng[1] - x1_arr[z]
        c = x2_arr[z] - x2_rng[0]
        d = c*b/a
        x2_arr[z] = x1_arr[z] + d


data_pt_cnt = 101
# The expected x-axis array (normalize 0 to 1).
x_arr = np.linspace( 0, 1, data_pt_cnt  )
# The array to store the data.
Y = np.zeros( ( n, data_pt_cnt ) )
# The labels associated with the plots.
labels = 2*np.ones( n )


fourPts = np.zeros((4, 2))
fourPts[0][0] = x0;         fourPts[0][1] = y0
fourPts[3][0] = x3
poly_cfig = PolyDropFuncConfig()



# Create the linear drop plot data given the specified randomization parameters.
for i in range(n):

    # Segment connection points coordinate update.
    fourPts[1][0] = x1_arr[i];  fourPts[1][1] = y1_arr[i]
    fourPts[2][0] = x2_arr[i];  fourPts[2][1] = y2_arr[i]
    fourPts[3][1] = y3_arr[i]

    # Polynomial drop segment settings update.
    poly_cfig.x0 = x1_arr[i]
    poly_cfig.y0 = y1_arr[i]
    poly_cfig.x1 = x2_arr[i]
    poly_cfig.y1 = y2_arr[i]
    poly_cfig.z = z_arr[i]
    poly_cfig.u_start = u_start_arr[i]


    y_arr = gen_linPolyLin_plotData( fourPts, poly_cfig, x_arr )

    Y[i,:] = y_arr[:]


# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       LinPolyLin Function Randomized Data Set Save
# ======================================================================= >>>>>

overwrite = True

# Define the data save path and name.
save_dir = currentdir + '/data/norm_plot_data'
save_filestem = 'linPolyLin_data'
save_fileext = '.npz'
save_filename = save_filestem + save_fileext

# If overwrite flag is off, make a separate save from existing data.
if not overwrite:
    save_fullFileName = str( next_free_name( save_dir, save_filestem, save_fileext ) )
else:
    save_fullFileName = save_dir + '/' + save_filename

# Save the data at the designated data directory.
np.savez( save_fullFileName, X=x_arr, Y=Y, labels_plotType=labels )

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       Data Load And Plot Check
# ======================================================================= >>>>>

# Boolean flag for indicating whether to plot the saved data or not.
plot_data = True
if plot_data:
    
    # Load the data from the designated data directory.
    data_tmp = np.load( save_fullFileName )
    x_arr_load = data_tmp["X"]
    Y_load = data_tmp["Y"]
    labels_load = data_tmp["labels_plotType"]

    # Print the data and check for error.
    for y_arr_z in Y_load:
        plt.plot( x_arr_load, y_arr_z )
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("y = x")
    plt.grid(True)
    plt.show()

# ======================================================================= <<<<<


