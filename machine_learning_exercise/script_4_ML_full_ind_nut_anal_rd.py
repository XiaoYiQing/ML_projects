

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

nut_name_arr = df_nut_id_map["name"]
nut_id_arr = df_nut_id_map["nutrient_id"]
nut_id_cnt = len( nut_id_arr )



fd_gr_cnt = 5

# Generate the range for a pair of indices.
rg_pair = idxUtils.gen_range_pair( range(fd_gr_cnt), range(fd_gr_cnt) )

# Generate the cumulative accuracy data array.
acc_np_arr = np.array( [[[None] * fd_gr_cnt] * fd_gr_cnt ] * nut_id_cnt )
acc_gr1_np_arr = np.array( [[[None] * fd_gr_cnt] * fd_gr_cnt ] * nut_id_cnt )
acc_gr2_np_arr = np.array( [[[None] * fd_gr_cnt] * fd_gr_cnt ] * nut_id_cnt )



# Define the data file name, which is to be located at the same directory as this
# script.
tar_file_name = f"{currentdir}/ML_5fdGr_ind_nut_acc_res.dat"


# Load from the data file (rb = Read binary).
fr = open( tar_file_name, "rb" )
acc_np_arr = pickle.load( fr )
acc_gr1_np_arr = pickle.load( fr )
acc_gr2_np_arr = pickle.load( fr )
fr.close()





gr_id_pair_arr = 1

# Compute the number of unique food group pairings.
uniq_pair_cnt = idxUtils.seq_lazy_caterer( fd_gr_cnt - 1 ) - 1

# Initialize accuracy array with no repeat of combination of food groups.
# Pairings from both order (such as pairs [1,2] and [2,1]) are averaged out.
acc_np_redux_arr = np.array( [ [None] * uniq_pair_cnt ] * nut_id_cnt )


for z in range( nut_id_cnt ):

    acc_np_z = acc_np_arr[z,:,:]

    z3 = 0
    for z1 in range( 0, fd_gr_cnt ):
        for z2 in range( z1 + 1, fd_gr_cnt ):

            # Average out the two pairings which only differ by ordering.
            acc_np_z_tar_avg = ( acc_np_z[z1,z2] + acc_np_z[z2,z1] )/2
            acc_np_redux_arr[z,z3] = acc_np_z_tar_avg
            
            z3 = z3 + 1

# Create array for labeling the data columns with the food group pairings.
pair_name_arr = np.array( [None] * uniq_pair_cnt )
z3 = 0
for z1 in range( 0, fd_gr_cnt ):
    for z2 in range( z1 + 1, fd_gr_cnt ):
        pair_name_arr[z3] = f"[{z1},{z2}]"
        z3 = z3 + 1


acc_np_redux_df = pd.DataFrame( acc_np_redux_arr, \
    index = nut_id_arr, \
    columns = pair_name_arr )



tmp = acc_np_redux_df[ pair_name_arr[0] ].copy( deep=True )

tmp.sort_values( ascending=False, inplace=True )
#print(tmp)
#print( tmp.iloc[0:3] )
#print( tmp.index[0:3] )

# Define the number of highest accuracy cases to retain.
top_cnt = 1
lmao = np.array( [[0]*top_cnt]*uniq_pair_cnt )

for z in range( uniq_pair_cnt ):
    
    pair_z_acc = acc_np_redux_df[ pair_name_arr[z] ].copy( deep = True )
    pair_z_acc.sort_values( ascending=False, inplace=True )
    #print( pair_z_acc.index[0:top_cnt] )
    tmp = pair_z_acc.index[0:top_cnt]

    lmao[ z, : ] = tmp[:]

print( lmao )

print( np.unique( lmao ) )