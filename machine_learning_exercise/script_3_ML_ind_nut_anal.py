


import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pprint
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

print( ML_runner )

# # Set the participating nutrients.
# ML_runner.nut_id_list = np.array( [1098] )

# ML_res = ML_runner.logRegr_2comp( 1, 3 )

# print( ML_res.get_gr1_name() )
# print( ML_res.get_gr2_name() )

# # print( ML_full_eval_res["pred_right"] )
# print( ML_res.get_acc() )
# print( ML_res.get_acc_gr1() )
# print( ML_res.get_acc_gr2() )

# # print( ML_setup.keys() )
# print( ML_res.get_train_gr1_nut() )
# print( ML_res.get_train_gr2_nut() )




fd_gr_cnt = 5
acc_np_arr = np.array( [[None] * fd_gr_cnt] * fd_gr_cnt )
acc_gr1_np_arr = np.array( [[None] * fd_gr_cnt] * fd_gr_cnt )
acc_gr2_np_arr = np.array( [[None] * fd_gr_cnt] * fd_gr_cnt )

    
ML_runner.nut_id_list = np.array( [1003] )

# Generate the range for a pair of indices.
rg_pair = idxUtils.gen_range_pair( range(fd_gr_cnt), range(fd_gr_cnt) )

# Define number of times the ML process is run.
repeat_cnt = 5

for gr_id_pair in rg_pair:

    gr1_id = gr_id_pair[0]
    gr2_id = gr_id_pair[1]

    acc = 0
    acc_gr1 = 0
    acc_gr2 = 0

    for z in range( repeat_cnt ):

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

    acc_np_arr[gr1_id][gr2_id] = acc
    acc_gr1_np_arr[gr1_id][gr2_id] = acc_gr1
    acc_gr2_np_arr[gr1_id][gr2_id] = acc_gr2        
            
                
            
tmp = pd.DataFrame(acc_np_arr)
print(tmp)



