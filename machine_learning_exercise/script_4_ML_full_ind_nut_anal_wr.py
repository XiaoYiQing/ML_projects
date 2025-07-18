

'''
This script is to create accuracy data for evaluating how well does
the logic regression ML method separate food items between two food
categories.

There are 5 food categories in this framework:
    > [index = 0] Fruits \n
    > [index = 1] Vegetables \n
    > [index = 2] Grains            \n
    > [index = 3] Protein Foods     \n
    > [index = 4] Dairy             \n

Each group has already a base set of food items that are partitioned into a
training and a testing set.
All permutations of group pairings (except self pairings) are verified for 
categorization accuracy, and the cumulation data is stored in a '.dat' file.
'''

import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn import linear_model
from sklearn import metrics

import foodDataParser as fdPar
from machine_learning_exercise.ML_5fdGr import ML_5fdGr_runner
from toolbox import indexingUtils as idxUtils



ML_runner = ML_5fdGr_runner()

# Define the utility subdirectory for this class
util_dir = f"{currentdir}/foodDataParser_util"

# Obtain the dataframe of nutritients that are recognized by this class.
df_nut_id_map = pd.read_csv( f"{util_dir}\\key_nutrient_id_map.csv" )

nut_id_arr = df_nut_id_map["nutrient_id"]
nut_id_cnt = len( nut_id_arr )



fd_gr_cnt = 5

# Generate the range for a pair of indices.
rg_pair = idxUtils.gen_range_pair( range(fd_gr_cnt), range(fd_gr_cnt) )

# Generate the cumulative accuracy data array.
acc_np_arr = np.array( [[[None] * fd_gr_cnt] * fd_gr_cnt ] * nut_id_cnt )
acc_gr1_np_arr = np.array( [[[None] * fd_gr_cnt] * fd_gr_cnt ] * nut_id_cnt )
acc_gr2_np_arr = np.array( [[[None] * fd_gr_cnt] * fd_gr_cnt ] * nut_id_cnt )


for z1 in range( nut_id_cnt ):

    # Set the current nutrient as the sole nutrient participating in the ML process.
    nut_id_z1 = nut_id_arr[z1]
    ML_runner.nut_id_list = [nut_id_z1]

    # Setup the variables to fill for the current nutrient ML run.
    acc_np_arr_z = np.array( [[None] * fd_gr_cnt] * fd_gr_cnt )
    acc_gr1_np_arr_z = np.array( [[None] * fd_gr_cnt] * fd_gr_cnt )
    acc_gr2_np_arr_z = np.array( [[None] * fd_gr_cnt] * fd_gr_cnt )

    # Define number of times the ML process is run.
    repeat_cnt = 5

    for gr_id_pair in rg_pair:
        
        # Obtain the current food group IDs.
        gr1_id = gr_id_pair[0]
        gr2_id = gr_id_pair[1]

        # Reset the accuracy values.
        acc = 0
        acc_gr1 = 0
        acc_gr2 = 0

        for z2 in range( repeat_cnt ):

            ML_res = ML_runner.logRegr_2comp( gr1_id, gr2_id )

            if ML_res is not None:
                
                acc = acc + ML_res.get_acc()
                acc_gr1 = acc_gr1 + ML_res.get_acc_gr1()
                acc_gr2 = acc_gr2 + ML_res.get_acc_gr2()

            else:
                
                acc = acc - 1
                acc_gr1 = acc_gr1 - 1
                acc_gr2 = acc_gr2 - 1

        acc = acc/repeat_cnt
        acc_gr1 = acc_gr1/repeat_cnt
        acc_gr2 = acc_gr2/repeat_cnt

        acc_np_arr_z[gr1_id][gr2_id] = acc
        acc_gr1_np_arr_z[gr1_id][gr2_id] = acc_gr1
        acc_gr2_np_arr_z[gr1_id][gr2_id] = acc_gr2        
                
                    
    acc_np_arr[ z1, :, : ] = acc_np_arr_z
    acc_gr1_np_arr[ z1, :, : ] = acc_gr1_np_arr_z
    acc_gr2_np_arr[ z1, :, : ] = acc_gr2_np_arr_z




# Define the data file name, which is to be located at the same directory as this
# script.
tar_file_name = f"{currentdir}/ML_5fdGr_ind_nut_acc_res.dat"

# Write to file (wb = write to binary).
fw = open( tar_file_name, "wb")
pickle.dump( acc_np_arr, fw )
pickle.dump( acc_gr1_np_arr, fw )
pickle.dump( acc_gr2_np_arr, fw )
fw.close()