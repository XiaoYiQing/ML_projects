
'''
This script runs a Machine Learning (ML) simulation which goal is to build
a model that can differentiate vegetable from protein based food.

The ML algorithm used use the logistic regression algorithm.
'''

import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath( os.path.join(currentdir, src) ) )


import numpy as np
import pandas as pd
from sklearn import linear_model

import foodDataParser as fdPar
from toolbox import indexingUtils as idxUtils



parser = fdPar.foodDataParser()

# The name of the directory where the food database csv files are located.
dirName = os.path.dirname(__file__)

# The name of the sub-directory for initialization files for Machine Learning 
# codes.
subdirName = 'ML_init_files'



init_file_names = [None]*5
init_file_names[0] = f"{dirName}\\{subdirName}\\init_food_fruits.csv"
init_file_names[1] = f"{dirName}\\{subdirName}\\init_food_vegetables.csv"
init_file_names[2] = f"{dirName}\\{subdirName}\\init_food_grains.csv"
init_file_names[3] = f"{dirName}\\{subdirName}\\init_food_proteinFoods.csv"
init_file_names[4] = f"{dirName}\\{subdirName}\\init_food_dairy.csv"


# ======================================================================= >>>>>
#   Food Group ID Array Setup
# ======================================================================= >>>>>
# Obtain the specific column with the food IDs and put it in a numpy array.
vegFd_df = pd.read_csv( init_file_names[1] )
vegFd_id = vegFd_df['fdc_id'].to_numpy()

# Obtain the specific column with the food IDs and put it in a numpy array.
proFd_df = pd.read_csv( init_file_names[3] )
proFd_id = proFd_df['fdc_id'].to_numpy()


# Subdivide the initial data set into the training set and the test set.
subdiv_sch_id = 1

# Ever other entry into the training set.
if subdiv_sch_id == 0:

    train_vegFd_id = vegFd_id[range(0,len(vegFd_id),2)]
    test_vegFd_id = vegFd_id[range(1,len(vegFd_id),2)]
    train_proFd_id = proFd_id[range(0,len(proFd_id),2)]
    test_proFd_id = proFd_id[range(1,len(proFd_id),2)]

# Random entries into the training set.
elif subdiv_sch_id == 1:

    train_set_cnt = 12
    tmp_ans = idxUtils.rand_samp( len( vegFd_id ), train_set_cnt )

    veg_train_idx = tmp_ans[0]
    veg_test_idx = tmp_ans[1]
    train_vegFd_id = vegFd_id[veg_train_idx]
    test_vegFd_id = vegFd_id[veg_test_idx]

    train_set_cnt = 12
    tmp_ans = idxUtils.rand_samp( len( proFd_id ), train_set_cnt )
    pro_train_idx = tmp_ans[0]
    pro_test_idx = tmp_ans[1]
    train_proFd_id = proFd_id[pro_train_idx]
    test_proFd_id = proFd_id[pro_test_idx]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#   Data Preparation
# ======================================================================= >>>>>

# The format of the nutrient information extracted. 
# This format MUST be kept consistent throughout the entire script.
nut_format_id = 3

# Obtain nutrient training sets.
train_vegFd_nut = parser.find_fd_gr_preset_nut( train_vegFd_id, nut_format_id = nut_format_id )
train_proFd_nut = parser.find_fd_gr_preset_nut( train_proFd_id, nut_format_id = nut_format_id )

# Obtain nutrient testing sets.
test_vegFd_nut = parser.find_fd_gr_preset_nut( test_vegFd_id, nut_format_id = nut_format_id )
test_proFd_nut = parser.find_fd_gr_preset_nut( test_proFd_id, nut_format_id = nut_format_id )

# Combine the training subsets into the full training set.
train_Fd_nut = np.concatenate( (train_vegFd_nut, train_proFd_nut), axis = 0 )
# ======================================================================= <<<<<


# ======================================================================= >>>>>
#   Logistic Regression Run
# ======================================================================= >>>>>
# y represents whether or not the food is a vegetable.
y_veg = np.array( [1]*len( train_vegFd_id ) )
y_prot = np.array( [0]*len( train_proFd_id ) )
y_all = np.concatenate( ( y_veg, y_prot ), axis = 0 )

# From the sklearn module we will use the LogisticRegression() method to 
# create a logistic regression object.
logr = linear_model.LogisticRegression()
# This object has a method called fit() that takes the independent and 
# dependent values as parameters and fills the regression object with data 
# that describes the relationship:
logr.fit( train_Fd_nut , y_all )
print( f"Number of iterations for convergence: {logr.n_iter_}" )



# Predict using the test sets.
veg_pred_res = logr.predict( test_vegFd_nut )
pro_pred_res = logr.predict( test_proFd_nut )
print( veg_pred_res )
print( pro_pred_res )

# Obtain boolean array for wrong results for the predictions.
veg_pred_err = veg_pred_res == 0
pro_pred_err = pro_pred_res == 1

# Obtain the fdc_id of the food being erroneously labelled.
veg_pred_err_fdc_id = test_vegFd_id[veg_pred_err]
pro_pred_err_fdc_id = test_proFd_id[pro_pred_err]


if len( veg_pred_err_fdc_id ) > 0:
    # Print a sample of wrongly labelled food.
    err_food = parser.findFood_nutrients( fdc_id = veg_pred_err_fdc_id[0] )
    print( err_food )
    print( err_food.get_preset_nut( 3 ) )
else:
    print( "No erroneous vegetable food labeling detected." )


if len( pro_pred_err_fdc_id ) > 0:
    err_food = parser.findFood_nutrients( fdc_id = pro_pred_err_fdc_id[0] )
    print( err_food )
    print( err_food.get_preset_nut( 3 ) )
else:
    print( "No erroneous protein food detected." )

# ======================================================================= <<<<<


