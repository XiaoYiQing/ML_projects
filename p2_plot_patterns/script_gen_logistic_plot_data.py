

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


from plot_funcs import LogisticFuncConfig
from plot_funcs import fit_logistic_2_pts
from plot_funcs import get_logistic_plot_data
from plot_funcs_data_gen import randDGen_logistic
from toolbox.file_nav import next_free_name
from toolbox.file_nav import file_exists



# ======================================================================= >>>>>
#       Logistic Function Randomized Data Set Gen
# ======================================================================= >>>>>

# Define the number of random test cases.
n = 3000

# The absolute x limit to the drop's defining points.
x_drop_rng_lim = ( 0.02, 0.98 )

# The range of mid points allowed.
drop_mid_pt_rng = ( 0.20, 0.80 )
# The range of width the logistic drop is allowed.
drop_width_rng = ( 0.10, 0.40 )

# The range of y starting value (highest point)
y_max_rng = ( 0.95, 1.00 )
# The range of y ending value (lowest point)
y_min_rng = ( 0.00, 0.05 )

# The slight dip in y from its highest point to the point where the main drop occurs.
y_pre_drop_dip_rng = ( 0.01, 0.05 )
# The slight dip in y from where the main drop ends to the lowest y value.
y_post_drop_dip_rng = ( 0.01, 0.05 )

data_pt_cnt = 251
# The expected x-axis array (normalize 0 to 1).
x_arr = np.linspace( 0, 1, data_pt_cnt )

dataGenObj = randDGen_logistic( x_drop_rng_lim, drop_mid_pt_rng, drop_width_rng, \
    y_max_rng, y_min_rng, y_pre_drop_dip_rng, y_post_drop_dip_rng )

Y, _, refPts_arr = dataGenObj.gen_data( n, x_arr )

# The labels associated with the plots (all zeros because gradual drop).
labels_plotType = np.zeros( n )
# The labels associated with the plot's drop identifying points.
labels_refXs = np.zeros( ( n, 2 ) )

# Create the logistic plot data given the specified randomization parameters.
for z in range(n):

    labels_refXs[z][0] = refPts_arr[z][0]
    labels_refXs[z][1] = refPts_arr[z][2]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Logistic Function Randomized Data Set Save
# ======================================================================= >>>>>

overwrite = True

# Define the data save path and name.
save_dir = currentdir + '/data/norm_plot_data'
save_filestem = 'logistic_drop_data'
save_fileext = '.npz'
save_filename = save_filestem + save_fileext

# If overwrite flag is off, make a separate save from existing data.
if not overwrite:
    save_fullFileName = str( next_free_name( save_dir, save_filestem, save_fileext ) )
else:
    save_fullFileName = save_dir + '/' + save_filename

# Save the data at the designated data directory.
np.savez( save_fullFileName, X=x_arr, Y=Y, labels_plotType=labels_plotType, labels_refXs=labels_refXs )

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