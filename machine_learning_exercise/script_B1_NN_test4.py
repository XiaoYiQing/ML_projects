

'''
test2:
    added more information printed for error cases in the

test3:
    Utilizes a more select array of features.
    Normalization is correct now and in effect by default.

test4:
    multiclass neural network
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


fdc_id_arr_list = []
y_arr_list = []

for z in range( len( init_file_names ) ):
    data_z = pd.read_csv( init_file_names[ z ] )
    fdc_id_arr_z = data_z['fdc_id'].to_numpy()
    yz = [z] * fdc_id_arr_z.size
    fdc_id_arr_list.append( fdc_id_arr_z )
    y_arr_list.append( yz )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#   Data partitioning
# ======================================================================= >>>>>

nut_id_preset = food.get_preset_nut_id( preset_id = 4 )

tr_frac = 0.6
test_frac = 0.02

fdc_train = np.zeros(0)
fdc_cv = np.zeros(0)
fdc_test = np.zeros(0)
y_train = np.zeros(0)
y_cv = np.zeros(0)
y_test = np.zeros(0)

for z in range( len( init_file_names ) ):

    # Fruits
    fdc_z_train, fdc_f_, yz_train, yf_ = train_test_split( fdc_id_arr_list[z], y_arr_list[z], \
        test_size = ( 1.0 - tr_frac ), random_state = 1 )
    fdc_z_cv, fdc_z_test, yz_cv, yz_test = train_test_split( fdc_f_, yf_, \
        test_size = test_frac, random_state = 1 )

    fdc_train = np.append( fdc_train, fdc_z_train, axis=0 )
    fdc_cv = np.append( fdc_cv, fdc_z_cv, axis=0 )
    fdc_test = np.append( fdc_test, fdc_z_test, axis=0 )
    y_train = np.append( y_train, yz_train, axis=0 )
    y_cv = np.append( y_cv, yz_cv, axis=0 )
    y_test = np.append( y_test, yz_test, axis=0 )



# Obtain the nutrition data using the arrays of food IDs.
X_train = parser.find_fd_gr_nut( fdc_train, nut_id_list = nut_id_preset )
X_cv = parser.find_fd_gr_nut( fdc_cv, nut_id_list = nut_id_preset )
X_test = parser.find_fd_gr_nut( fdc_test, nut_id_list = nut_id_preset )


use_norm = True
if( use_norm ):
    # Normalize the features.
    # X_tr_norm, X_mu, X_sigma = zscore_normalize_features(X_train)
    X_tr_norm, max_tmp, min_tmp = minmax_normalize_features(X_train)
    X_cv_norm = ( X_cv - min_tmp )/( max_tmp - min_tmp )
    X_test_norm = ( X_test - min_tmp )/( max_tmp - min_tmp )

else:
    X_tr_norm = X_train
    X_cv_norm = X_cv
    X_test_norm = X_test


# ======================================================================= <<<<<




# ======================================================================= >>>>>
#   Neural Network Build and Train
# ======================================================================= >>>>>

model = Sequential(
    [               
        ### START CODE HERE ### 
        tf.keras.Input(shape=( np.shape( X_tr_norm )[1] , )),    #specify input shape
        Dense( len( nut_id_preset ), activation = "relu", name = "L1" ),
        Dense( 40, activation = "relu", name = "L2" ),
        Dense( 20, activation = "relu", name = "L3" ),
        Dense( 5, activation = "linear", name = "L4" ),
        ### END CODE HERE ### 
    ], name = "my_model" 
)

model.summary()

model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.002),
)

history = model.fit(
    X_tr_norm,y_train,
    epochs=300,
    verbose=0
)

print("Training Loss (last epoch):", history.history['loss'][-1])
# ======================================================================= <<<<<



print(f"X train shape: {np.shape( X_tr_norm )}")
print(f"Y train shape: {np.shape( y_train )}")

print( f"Train size: {np.shape( X_tr_norm )[0]}" )
print( f"CV size: {np.shape( X_cv_norm )[0]}" )
print( f"Test size: {np.shape( X_test_norm )[0]}" )

print()




y_pred = [-1]*len( y_cv )
wrong_cnt = 0
fdc_wrong_arr = [-1.0]*len( y_cv )

for z in range( np.shape( X_cv_norm )[0] ):

    X_z = X_cv_norm[ z, : ].reshape( 1, -1 )
    y_z = y_cv[ z ]
    prediction_z = model.predict( X_z, verbose=0 )
    prediction_p_z = tf.nn.softmax( prediction_z )

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