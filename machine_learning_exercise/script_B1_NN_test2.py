'''
This script is to practice using neural network in creating a prediction function
that predicts whether a food item belongs to a target food group based on the
nutrients of this food.

test2:
    added more information printed for error cases in the 
'''



import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.activations import linear, relu, sigmoid
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


import foodDataParser as fdPar
from foodDataParser import food
from machine_learning_exercise.ML_5fdGr import ML_5fdGr_runner
from toolbox import indexingUtils as idxUtils
from toolbox.dataUtils import zscore_normalize_features
from toolbox.dataUtils import minmax_normalize_features

parser = fdPar.foodDataParser()

# This file's directory location shall be the root of all other relative pathing
# defined here.
dirName = os.path.dirname(__file__)


# ======================================================================= >>>>>
#   Food List Initialization
# ======================================================================= >>>>>

# Food ID initialization files.
init_file_names = [None]*5
init_file_names[0] = f"{dirName}\\ML_init_files\\init_food_fruits.csv"
init_file_names[1] = f"{dirName}\\ML_init_files\\init_food_vegetables.csv"
init_file_names[2] = f"{dirName}\\ML_init_files\\init_food_grains.csv"
init_file_names[3] = f"{dirName}\\ML_init_files\\init_food_proteinFoods.csv"
init_file_names[4] = f"{dirName}\\ML_init_files\\init_food_dairy.csv"    


# Define the target food group index.
# The foods of this target group are considered "Correct".
tar_fd_gr_idx = 1


fdc_id_arr_f = np.zeros(0)
yf = np.zeros(0)
for z in range( len(init_file_names) ):

    if( z == tar_fd_gr_idx ):
        continue

    # Obtain the array of food indices.
    data_z = pd.read_csv( init_file_names[z] )
    fdc_id_arr_z = data_z['fdc_id'].to_numpy()
    # Initialize the value of the current group to 0 ("Incorrect").
    y_z = [0] * fdc_id_arr_z.size

    # Append the current food index array and its corresponding value array to the full group.
    fdc_id_arr_f = np.append( fdc_id_arr_f, fdc_id_arr_z )
    yf = np.append( yf, y_z )



# Obtain the food index array and its corresponding value array of the target food group.
data_z = pd.read_csv( init_file_names[ tar_fd_gr_idx ] )
fdc_id_arr_t = data_z['fdc_id'].to_numpy()
yt = [1] * fdc_id_arr_t.size

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#   Data partitioning
# ======================================================================= >>>>>

nut_id_preset = food.get_preset_nut_id( preset_id = 1 )

tr_frac = 0.6
test_frac = 0.1

fdc_f_train, fdc_f_, yf_train, yf_ = train_test_split( fdc_id_arr_f, yf, \
    test_size = ( 1.0 - tr_frac ), random_state = 1 )
fdc_f_cv, fdc_f_test, yf_cv, yf_test = train_test_split( fdc_f_, yf_, \
    test_size = test_frac, random_state = 1 )
fdc_t_train, fdc_t_, yt_train, yt_ = train_test_split( fdc_id_arr_t, yt, \
    test_size = ( 1.0 - tr_frac ), random_state = 1 )
fdc_t_cv, fdc_t_test, yt_cv, yt_test = train_test_split( fdc_t_, yt_, \
    test_size = test_frac, random_state = 1 )

fdc_train = np.append( fdc_f_train, fdc_t_train, axis=0 )
y_train = np.append( yf_train, yt_train )
fdc_cv =  np.append( fdc_f_cv, fdc_t_cv, axis=0 )
y_cv =  np.append( yf_cv, yt_cv )
fdc_test =  np.append( fdc_f_test, fdc_t_test, axis=0 )
y_test =  np.append( yf_test, yt_test )


X_train = parser.find_fd_gr_nut( fdc_train, nut_id_list = nut_id_preset )
X_cv = parser.find_fd_gr_nut( fdc_cv, nut_id_list = nut_id_preset )
X_test = parser.find_fd_gr_nut( fdc_test, nut_id_list = nut_id_preset )


use_norm = False
if( use_norm ):
    # Normalize the features.
    # X_tr_norm, X_mu, X_sigma = zscore_normalize_features(X_train)
    X_tr_norm, max_tmp, min_tmp = minmax_normalize_features(X_train)
else:
    X_tr_norm = X_train

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#   Neural Network Build and Train
# ======================================================================= >>>>>

model = Sequential(
    [               
        ### START CODE HERE ### 
        tf.keras.Input(shape=( np.shape( X_tr_norm )[1] , )),    #specify input shape
        Dense( len( nut_id_preset ), activation = "relu", name = "L1" ),
        Dense( 25, activation = "relu", name = "L2" ),
        Dense( 15, activation = "relu", name = "L3" ),
        Dense( 2, activation = "linear", name = "L4" ),
        ### END CODE HERE ### 
    ], name = "my_model" 
)

model.summary()

model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
)

history = model.fit(
    X_tr_norm,y_train,
    epochs=70
)

# ======================================================================= <<<<<


print(f"X train shape: {np.shape( X_tr_norm )}")
print(f"Y train shape: {np.shape( y_train )}")

print( f"Train size: {np.shape( X_tr_norm )[0]}" )
print( f"CV size: {np.shape( X_cv )[0]}" )
print( f"Test size: {np.shape( X_test )[0]}" )

print()


y_pred = [-1]*len( y_cv )
wrong_cnt = 0
fdc_wrong_arr = [-1.0]*len( y_cv )

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" # Only errors are logged

for z in range( np.shape( X_cv )[0] ):

    X_z = X_cv[ z, : ].reshape( 1, -1 )
    y_z = y_cv[ z ]
    prediction_z = model.predict( X_z )
    prediction_p_z = tf.nn.softmax(prediction_z)

    yhat_z = np.argmax( prediction_p_z )

    y_pred[z] = yhat_z

    print( "Softmax prediction: ", end = "" )
    print( prediction_p_z )
    print( f"[np.argmax(prediction_p): {yhat_z}]", end = "    " )
    print( f"[True y: {y_z}]" )

    if( yhat_z != y_z ):
        fdc_wrong_arr[wrong_cnt] = fdc_cv[z]
        wrong_cnt += 1
        

fdc_wrong_arr = fdc_wrong_arr[0:wrong_cnt]

print( f"Wrong count: {wrong_cnt}" )
print( f"Wrong food fdc list: {fdc_wrong_arr}" )

X_wrong = parser.find_fd_gr_nut( fdc_wrong_arr, nut_id_list = nut_id_preset )


for z in range( wrong_cnt ):
    tmp = parser.findFood_nutrients( fdc_id = fdc_wrong_arr[z] )
    print( tmp )
    nut_tmp = tmp.get_nutrients( nut_id_list = nut_id_preset )
    print( nut_tmp )
