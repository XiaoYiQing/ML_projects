

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
from plot_funcs_data_gen import randDGen_LPL

from toolbox.file_nav import next_free_name
from toolbox.file_nav import file_exists



# ======================================================================= >>>>>
#       Randomized Data Set Gen
# ======================================================================= >>>>>

# Define the number of random test cases.
n = 2000

# The two delimiting x values over the range this LPL function is defined.
x_ref = ( 0, 1 )
# Poly drop start point x range.
x1_rng = ( 0.01, 0.50 )
# Poly drop end point range.
x2_rng = ( 0.30, 0.80 )

y_rngs = np.array([
    [0.99, 1.00],   # Plot starting y range.
    [0.95, 0.99],   # Poly drop start point y range.
    [0.20, 0.06],   # Poly drop end point y range.
    [0.01, 0.05]    # End y value range of the trailing linear segment.
])

# Polynomial degree range.
z_rng = ( 1.5, 10 )
# Range of percentage of poly drop portion forced being flat.
u_start_rng = ( 0.05, 0.7 )

data_pt_cnt = 101
# The expected x-axis array (normalize 0 to 1).
x_arr = np.linspace( 0, 1, data_pt_cnt )

# Create the plot data generation object.
dataGenObj = randDGen_LPL( x_ref, x1_rng, x2_rng, y_rngs, z_rng, u_start_rng )

# Perform the randomized data generation.
Y, polyCFig_arr = dataGenObj.gen_data( n, x_arr )

# The labels associated with the plots.
labels = 2*np.ones( n )

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


