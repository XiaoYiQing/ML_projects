

'''
In this script, we finally gather all piecewise acquired information on which
features to be used to determine the food category of a food item.

The features from each pairing of food group comparsion are all put together in
this script to create a final neural network that can distinguish the category of 
a food based on the selected nutritients/features to represent it.

What I learned:
- To gradually assemble features using sub-neural networks which compare subsets of
    outcomes is a good way to reach a final robust neural network.
    It seems that the final NN solution can be reached through direct summation
    of the results of subset NNs.

NOTE: I deleted Water (id: 1050) and added sugar (id: 1063).
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
init_file_names[0] = f"{dirName}\\ML_init_files\\init_food_vegetables.csv"
init_file_names[1] = f"{dirName}\\ML_init_files\\init_food_fruits.csv"
init_file_names[2] = f"{dirName}\\ML_init_files\\init_food_grains.csv"
init_file_names[3] = f"{dirName}\\ML_init_files\\init_food_proteinFoods.csv"
init_file_names[4] = f"{dirName}\\ML_init_files\\init_food_dairy.csv"

# f"{dirName}\\ML_init_files\\init_food_fruits.csv"
# f"{dirName}\\ML_init_files\\init_food_vegetables.csv"
# f"{dirName}\\ML_init_files\\init_food_grains.csv"
# f"{dirName}\\ML_init_files\\init_food_proteinFoods.csv"
# f"{dirName}\\ML_init_files\\init_food_dairy.csv"    


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

# nut_id_preset = food.get_preset_nut_id( preset_id = 4 )

# veg vs fruit
# nut_id_preset = np.array( [ \
#     1071, 1094, 1097,  \
#     1002, 1003, 1011, 1032, 1039 ] )

# veg vs grain
# nut_id_preset = np.array( [ \
#     1010, 1012, 1050, 1094, 1097, 1137, 1146, 1162, \
#     1185, 2057, 2069, \
#     1165 ] )

#  fruit vs grain
# nut_id_preset = np.array( [ \
#     1002, 1003, 1011, 1032, 1039, 1050, 1082, 1084, \
#     1012, 1093, \
#     1170 ] )

# veg vs protein
# nut_id_preset = np.array( [ \
#     1009, 1079, 1050, 1094, 1097, \
#     1004, 1085, 1100, 1105, 1195, 1253 ] )
# fruit vs protein
# nut_id_preset = np.array( [ \
#     1002, 1003, 1011, 1032, 1039, 1050, 1082, 1084, \
#     1012, 1093, \
#     1004, 1085, 1100, 1105, 1195, 1253 ] )
# grain vs protein
# nut_id_preset = np.array( [ \
#     1005, 1009, 1093, 1106, 1109, 1170, \
#     1051, 1085, 1100, 1112, 1113, 1114, 1195, 1257, 1258 ] )

# protein vs dairy
# nut_id_preset = np.array( [ \
#     1079, 1089, 1090, 1098, 1253, \
#     1013, 1075, 1259, 1260, 1261, 1272 ] )
# fruit vs dairy
# nut_id_preset = np.array( [ \
#     1002, 1003, 1011, 1032, 1039, 1050, 1082, 1084, \
#     1012, 1093, \
#     1004, 1085, 1100, 1105, 1253, 1257, 1258 ] )
# veg vs dairy
# nut_id_preset = np.array( [ 1093, \
#     1009, 1079, 1050, 1094, 1097, \
#     1013, 1253, 1259 ] )
# grain vs dairy
# nut_id_preset = np.array( [ \
#     1009, 1079, 1089, 1093, 1098, 1106, 1109, \
#     1013, 1075, 1085 ] )

nut_id_preset = np.array( [ \
    1002, 1003, 1004, 1005, 1009, 1010, 1011, 1012, 1013, 1032, \
    1039, 1050, 1063, 1071, 1079, 1082, 1084, 1085, 1185, 1089, 1090, \
    1093, 1094, 1097, 1098, 1100, 1105, 1106, 1109, 1112, 1113, \
    1114, 1137, 1146, 1162, 1165, 1170, 1075, 1195, 1253, 1257, \
    1258, 1259, 1260, 1261, 1272, 2057, 2069 \
    ] )


tr_frac = 0.5
test_frac = 0.02

fdc_train = np.zeros(0)
fdc_cv = np.zeros(0)
fdc_test = np.zeros(0)
y_train = np.zeros(0)
y_cv = np.zeros(0)
y_test = np.zeros(0)

for z in range( len( init_file_names ) ):

    # Fruits
    # fdc_z_train, fdc_f_, yz_train, yf_ = train_test_split( fdc_id_arr_list[z], y_arr_list[z], \
    #     test_size = ( 1.0 - tr_frac ), random_state = 1 )
    fdc_z_train, fdc_f_, yz_train, yf_ = train_test_split( fdc_id_arr_list[z], y_arr_list[z], \
        test_size = ( 1.0 - tr_frac ) )
    # fdc_z_cv, fdc_z_test, yz_cv, yz_test = train_test_split( fdc_f_, yf_, \
    #     test_size = test_frac, random_state = 1 )
    fdc_z_cv, fdc_z_test, yz_cv, yz_test = train_test_split( fdc_f_, yf_, \
        test_size = test_frac )

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

reg_factor = 0.0001

model = Sequential(
    [               
        ### START CODE HERE ### 
        tf.keras.Input(shape=( np.shape( X_tr_norm )[1] , )),    #specify input shape
        Dense( len( nut_id_preset ), activation = "relu", name = "L1" ),
        Dense( 70, activation = "relu", name = "L2", \
            kernel_regularizer=tf.keras.regularizers.l2( reg_factor ) ),
        Dense( 35, activation = "relu", name = "L3", \
            kernel_regularizer=tf.keras.regularizers.l2( reg_factor ) ),
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
    epochs=500,
    verbose=1
)

print("Training Loss (last epoch):", history.history['loss'][-1])

print(f"X train shape: {np.shape( X_tr_norm )}")
print(f"Y train shape: {np.shape( y_train )}")

print( f"Train size: {np.shape( X_tr_norm )[0]}" )
print( f"CV size: {np.shape( X_cv_norm )[0]}" )
print( f"Test size: {np.shape( X_test_norm )[0]}" )

print()

# ======================================================================= <<<<<









# ======================================================================= >>>>>
#   Cross-Validation
# ======================================================================= >>>>>

#make a model for plotting routines to call
model_predict_s = lambda Xl: tf.nn.softmax(model.predict(Xl)).numpy()
# model_predict_s = lambda Xl: np.argmax(tf.nn.softmax(model.predict(Xl)).numpy(),axis=1)

# Use the model to predict the cross-validation sample set.
y_tmp = model_predict_s( X_cv_norm )
# Obtain the highest prediction out of the classes.
y_pred = np.argmax( y_tmp, axis=1 )

# Determine the errors.
y_err = y_cv != y_pred


# Obtain the food indices of the wrong predictions.
fdc_wrong_arr = fdc_cv[ y_err ]
wrong_cnt = np.sum( y_err )

# Print the wrongly predicted food details.
for z in range( wrong_cnt ):
    tmp = parser.findFood_nutrients( fdc_id = fdc_wrong_arr[z] )
    print( tmp )
    nut_tmp = tmp.get_nutrients( nut_id_list = nut_id_preset )
    print( nut_tmp )

print( f"Wrong count: {wrong_cnt}" )


# ======================================================================= <<<<<
