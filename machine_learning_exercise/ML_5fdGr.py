


import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier

import foodDataParser as fdPar
from foodDataParser import food
from toolbox import indexingUtils as idxUtils
from toolbox import pandasUtils as pdUtils


class ML_5fdGr_runner:
    '''
    This class is a specialized class for facilitation generation of 
    Machine Learning (ML) model for the specific task of determining the food 
    category to which a food item belongs to based on the nutrients of the said food. 

    The food categories definition used are: 
        > [index = 0] Fruits \n
        > [index = 1] Vegetables \n
        > [index = 2] Grains            \n
        > [index = 3] Protein Foods     \n
        > [index = 4] Dairy             \n
    This class uses relative directory pathing to obtain the necessary data to 
    conduct the ML process, so the file in which this class is defined must
    be within the same directory as a multitude of csv files as well as support python files.

    As such, this class cannot be simply copied pasted away as a stand alone. 
    Sorry for the inconvenience.
    '''

    # This file's directory location shall be the root of all other relative pathing
    # defined here.
    dirName = os.path.dirname(__file__)
    # The name of the sub-directory for initialization files for Machine Learning 
    # codes.
    subdirName = 'ML_init_files'

    def __init__( self, **args ):
        
        # Initialize the parser
        self.parser = fdPar.foodDataParser()

        # Food ID initialization files.
        init_file_names = [None]*5
        init_file_names[0] = f"{self.dirName}\\{self.subdirName}\\init_food_fruits.csv"
        init_file_names[1] = f"{self.dirName}\\{self.subdirName}\\init_food_vegetables.csv"
        init_file_names[2] = f"{self.dirName}\\{self.subdirName}\\init_food_grains.csv"
        init_file_names[3] = f"{self.dirName}\\{self.subdirName}\\init_food_proteinFoods.csv"
        init_file_names[4] = f"{self.dirName}\\{self.subdirName}\\init_food_dairy.csv"    
        self.init_file_names = init_file_names

        # Food group names.
        food_type_names = [None]*5
        food_type_names[0] = "Fruits"
        food_type_names[1] = "Vegetables"
        food_type_names[2] = "Grains"
        food_type_names[3] = "Protein Foods"
        food_type_names[4] = "Dairy"
        self.food_type_names = food_type_names


        # Training and test sets subdivision scheme id.
        # [1 = random, 2 = every other term]
        if "subdiv_sch_id" in args:
            self.subdiv_sch_id = args["subdiv_sch_id"]
        else:
            self.subdiv_sch_id = 1

        # Training sets and test sets sizes 
        # (NOTE: can be overriden depending on 'subdiv_sch_id').
        if "gr1_tr_set_cnt" in args:
            self.gr1_tr_set_cnt = args["gr1_tr_set_cnt"]
        else:
            self.gr1_tr_set_cnt = 10
        if "gr2_tr_set_cnt" in args:
            self.gr2_tr_set_cnt = args["gr2_tr_set_cnt"]
        else:
            self.gr2_tr_set_cnt = 10
        
        # Define the list of nutrient IDs that shall participate in the ML process.
        # Nurtients whose ID appear in this list will serve as variables in helping 
        # to differentiate foods from different food groups.
        if "nut_id_list" in args:
            self.nut_id_list = args["nut_id_list"]
        else:
            self.nut_id_list = food.get_preset_nut_id(3)

    def __str__( self ):

        # Print the information of the current food.
        str_ans = "Machine Learning Runner for 5 food groups:"
        str_ans = f"{str_ans}\n   Food Groups: {self.food_type_names}"
        str_ans = f"{str_ans}\n   Train and Test sets sudivision scheme ID: {self.subdiv_sch_id}"
        str_ans = f"{str_ans}\n   Train set size for group 1 and group 2: {self.gr1_tr_set_cnt}, {self.gr2_tr_set_cnt}"
        str_ans = f"{str_ans}\n   Participating nutrient ID list: {self.nut_id_list}"

        return str_ans


        x = 1



    def eval_model( self, model, test_fdc_id_set, y_true ):
        '''
        Evaluate the model using the given test set.
        Given the context where the ML model is used, the test set 'test_fdc_id_set' 
        is simply the array of food ID "fdc_id" and the expected outcome "y_true" is simply
        an array of 0 and 1, where 0 refers to the first food group and 1 refers to the 
        second food group used to construct the model.
        '''

        # Turn the fdc_id into an array of food nutrients.
        test_nut = self.parser.find_fd_gr_nut( test_fdc_id_set, \
            nut_id_list = self.nut_id_list )

        # Predict using the test sets.
        y_pred = model.predict( test_nut )

        # Obtain boolean array for wrong results for the predictions.
        pred_right = y_pred == y_true

        # Compute accuracy of prediction.
        right_cnt = pred_right.sum()
        accuracy = right_cnt/len( y_true )

        # Create confusion matrix/
        display_labels = [0, 1]
        conf_mat = metrics.confusion_matrix( y_true, y_pred, labels = display_labels )


        eval_res = {
        "test_nut": test_nut,
        "y_true": y_true,
        "y_pred": y_pred,
        "pred_right": pred_right,
        "accuracy": accuracy,
        "conf_mat": conf_mat
        }

        return eval_res

    def get_grX_fdc_id( self, grX_idx ):
        '''
        Obtain the fdc_id of the food items of the target food group.
        '''

        grX_df = pd.read_csv( self.init_file_names[grX_idx] )
        grX_id = grX_df['fdc_id'].to_numpy()

        return grX_id

    def get_arr_subdiv( self, fdc_id_arr ):
        '''
        Subdivide the array into a training set and a testing set following
        the subdivision scheme determined by "subdiv_sch_id" that the current class 
        object is set to.

        The training set is returned first.
        '''

        # Random entries into the training set.
        if self.subdiv_sch_id == 1:
            
            tmp_ans = idxUtils.rand_samp( len( fdc_id_arr ), self.gr1_tr_set_cnt )
            gr1_train_idx = tmp_ans[0]
            gr2_test_idx = tmp_ans[1]
            train_set = fdc_id_arr[gr1_train_idx]
            test_set = fdc_id_arr[gr2_test_idx]

        # Ever other entry into the training set.
        elif self.subdiv_sch_id == 2:
            
            train_set = fdc_id_arr[ range( 0, len( fdc_id_arr ), 2 ) ]
            test_set = fdc_id_arr[ range( 1, len( fdc_id_arr ), 2 ) ]


        return train_set, test_set


    def ML_2gr_prep( self, gr1_idx, gr2_idx ):
        '''
        Prepare the variables necessary for performing Machine Learning modeling
        process for the targeted two food groups.
        '''

        # Obtain the name of the two food groups.
        gr1_name = self.food_type_names[gr1_idx]
        gr2_name = self.food_type_names[gr2_idx]

        # Obtain food IDs of both food groups.
        gr1_fdc_id = self.get_grX_fdc_id( gr1_idx )
        gr2_fdc_id = self.get_grX_fdc_id( gr2_idx )

        # Subdivide both food groups into 
        [ train_gr1_id, test_gr1_id ] = self.get_arr_subdiv( gr1_fdc_id )
        [ train_gr2_id, test_gr2_id ] = self.get_arr_subdiv( gr2_fdc_id )

        # Obtain nutrient training sets.
        train_gr1_nut = self.parser.find_fd_gr_nut( train_gr1_id, \
            nut_id_list = self.nut_id_list )
        train_gr2_nut = self.parser.find_fd_gr_nut( train_gr2_id, \
            nut_id_list = self.nut_id_list )
        
        # Combine the training subsets into the full training set.
        full_train_set = np.concatenate( ( train_gr1_nut, train_gr2_nut ), axis = 0 )

        # y indicates if the food belongs to group 1 (0) or group 2 (1).
        gr1_y = np.array( [0]*len( train_gr1_id ) )
        gr2_y = np.array( [1]*len( train_gr2_id ) )
        y = np.concatenate( ( gr1_y, gr2_y ), axis = 0 )

        ML_setup = {
        "gr1_name": gr1_name,
        "gr2_name": gr2_name,
        "train_gr1_id": train_gr1_id,
        "train_gr2_id": train_gr2_id,
        "train_gr1_nut": train_gr1_nut,
        "train_gr2_nut": train_gr2_nut,
        "train_Fd_nut": full_train_set,
        "gr1_y": gr1_y,
        "gr2_y": gr2_y,
        "y": y,
        "test_gr1_id": test_gr1_id,
        "test_gr2_id": test_gr2_id,
        }

        return ML_setup



    def logRegr_2comp( self, gr1_idx, gr2_idx ):
        '''
        Function performing logistic regression between two food groups out of 
        the 5 food groups:
        The given two indices to this function will perform the logistic regression
        between the two associated food groups (Cannot be the same group).
        The food categories definition used are:
            > [index = 0] Fruits \n
            > [index = 1] Vegetables \n
            > [index = 2] Grains            \n
            > [index = 3] Protein Foods     \n
            > [index = 4] Dairy             \n
        '''

        if gr1_idx == gr2_idx:
            return None

        ML_setup = self.ML_2gr_prep( gr1_idx, gr2_idx )

        train_Fd_nut = ML_setup['train_Fd_nut']
        y = ML_setup['y']
        test_gr1_id = ML_setup['test_gr1_id']
        test_gr2_id = ML_setup['test_gr2_id']
        gr1_len = len( test_gr1_id )
        gr2_len = len( test_gr2_id )

        # From the sklearn module we will use the LogisticRegression() method to 
        # create a logistic regression object.
        logr = linear_model.LogisticRegression()
        # This object has a method called fit() that takes the independent and 
        # dependent values as parameters and fills the regression object with data 
        # that describes the relationship:
        logr.fit( train_Fd_nut , y )

        # Use the test sets to evaluate the model.
        # gr1_eval_res = self.eval_model( logr, test_gr1_id, [0]*len( test_gr1_id ) )
        # gr2_eval_res = self.eval_model( logr, test_gr2_id, [1]*len( test_gr2_id ) )
        
        # Create the full test set.
        test_all_id = np.append( test_gr1_id, test_gr2_id )
        # Create the full expected result set.
        y_expect = ( [0]*gr1_len ) + ( [1]*gr2_len )
        # Perfeorm prediction using the model and compute the results.
        full_eval_res = self.eval_model( logr, test_all_id, y_expect )

        # Obtain prediction evaluation results separately for each of the two 
        # food groups and add to the final evaluation result object.
        pred_right = full_eval_res["pred_right"]
        pred_right_gr1 = pred_right[ range( gr1_len ) ]
        pred_right_gr2 = pred_right[ range( gr1_len, gr1_len + gr2_len ) ]
        accuracy_gr1 = pred_right_gr1.sum()/gr1_len
        accuracy_gr2 = pred_right_gr2.sum()/gr2_len
        full_eval_res["pred_right_gr1"] = pred_right_gr1
        full_eval_res["pred_right_gr2"] = pred_right_gr2
        full_eval_res["accuracy_gr1"] = accuracy_gr1
        full_eval_res["accuracy_gr2"] = accuracy_gr2

        # Add the nutrients to the final evaluation result object.
        test_nut = full_eval_res["test_nut"]
        test_gr1_nut = test_nut[ range( gr1_len ), : ]
        test_gr2_nut = test_nut[ range( gr1_len, gr1_len + gr2_len ), : ]
        full_eval_res["test_gr1_nut"] = test_gr1_nut
        full_eval_res["test_gr2_nut"] = test_gr2_nut

        # The values in dictionary items can be of any data type:
        # ML_res = {
        # "model": logr,
        # "ML_setup": ML_setup,
        # "full_eval_res": full_eval_res
        # }

        ML_res = ML_5fdGr_res( logr, ML_setup, full_eval_res )

        return ML_res



    def decTree_2comp( self, gr1_idx, gr2_idx ):
        '''
        Function performing decision tree model for comparing two food groups out of 
        the 5 food groups:
        The given two indices to this function will perform the logistic regression
        between the two associated food groups (Cannot be the same group).
        The food categories definition used are:
            > [index = 0] Fruits \n
            > [index = 1] Vegetables \n
            > [index = 2] Grains            \n
            > [index = 3] Protein Foods     \n
            > [index = 4] Dairy             \n
        '''

        ML_setup = self.ML_2gr_prep( gr1_idx, gr2_idx )

        train_Fd_nut = ML_setup['train_Fd_nut']
        y = ML_setup['y']
        test_gr1_id = ML_setup['test_gr1_id']
        test_gr2_id = ML_setup['test_gr2_id']

        dtree = DecisionTreeClassifier()
        dtree = dtree.fit( train_Fd_nut, y )
        
        # Use the test sets to evaluate the model.
        gr1_eval_res = self.eval_model( dtree, test_gr1_id, [0]*len( test_gr1_id ) )
        gr2_eval_res = self.eval_model( dtree, test_gr2_id, [1]*len( test_gr2_id ) )

        # The values in dictionary items can be of any data type:
        ML_res = {
        "model": dtree,
        "ML_setup": ML_setup,
        "gr1_eval_res": gr1_eval_res,
        "gr2_eval_res": gr2_eval_res
        }

        return ML_res


    def hiera_cluster_2comp( self, gr1_idx, gr2_idx ):
        '''
        The given two indices to this function will perform Agglomerative Clustering
        between the two associated food groups (Cannot be the same group).
        The food categories definition used are:
            > [index = 0] Fruits \n
            > [index = 1] Vegetables \n
            > [index = 2] Grains            \n
            > [index = 3] Protein Foods     \n
            > [index = 4] Dairy             \n

        Note that this is an unsupervised Machine Learning method, so both "train" and test
        are performed on the same data.
        '''
        
        # Obtain the name of the two food groups.
        gr1_name = self.food_type_names[gr1_idx]
        gr2_name = self.food_type_names[gr2_idx]
        # Obtain food IDs of both food groups.
        gr1_fdc_id = self.get_grX_fdc_id( gr1_idx )
        gr2_fdc_id = self.get_grX_fdc_id( gr2_idx )

        # Obtain nutrient training sets.
        train_gr1_nut = self.parser.find_fd_gr_nut( gr1_fdc_id, \
            nut_id_list = self.nut_id_list )
        train_gr2_nut = self.parser.find_fd_gr_nut( gr2_fdc_id, \
            nut_id_list = self.nut_id_list )
        
        # Combine the training subsets into the full training set.
        full_train_set = np.concatenate( ( train_gr1_nut, train_gr2_nut ), axis = 0 )

        full_train_set_pd = pd.DataFrame( full_train_set )
        # Normalize the nutrients (per column)
        full_train_set_pd = pdUtils.norm_all_col( full_train_set_pd, norm_sch_id = 1 )

        hierarchical_cluster = AgglomerativeClustering(n_clusters = 4, \
            metric='euclidean', linkage='ward')
        y = hierarchical_cluster.fit_predict( full_train_set_pd )

        
        full_train_set_pd['Cluster'] = y


        y_gr1 = y[range( len( gr1_fdc_id ) )]
        y_gr2 = y[range( len( gr1_fdc_id ), len( gr1_fdc_id ) + len( gr2_fdc_id ) )]
        print( y_gr1 )
        print( y_gr2 )


    
    def K_means_2comp( self, gr1_idx, gr2_idx ):
        '''
        The given two indices to this function will perform K means clustering
        between the two associated food groups (Cannot be the same group).
        The food categories definition used are:
            > [index = 0] Fruits \n
            > [index = 1] Vegetables \n
            > [index = 2] Grains            \n
            > [index = 3] Protein Foods     \n
            > [index = 4] Dairy             \n

        Note that this is an unsupervised Machine Learning method, so both "train" and test
        are performed on the same data.
        '''

        # Obtain the name of the two food groups.
        gr1_name = self.food_type_names[gr1_idx]
        gr2_name = self.food_type_names[gr2_idx]
        # Obtain food IDs of both food groups.
        gr1_fdc_id = self.get_grX_fdc_id( gr1_idx )
        gr2_fdc_id = self.get_grX_fdc_id( gr2_idx )

        # Obtain nutrient training sets.
        train_gr1_nut = self.parser.find_fd_gr_nut( gr1_fdc_id, \
            nut_id_list = self.nut_id_list )
        train_gr2_nut = self.parser.find_fd_gr_nut( gr2_fdc_id, \
            nut_id_list = self.nut_id_list )
        
        # Combine the training subsets into the full training set.
        full_train_set = np.concatenate( ( train_gr1_nut, train_gr2_nut ), axis = 0 )

        full_train_set_pd = pd.DataFrame( full_train_set )
        # Normalize the nutrients (per column)
        full_train_set_pd = pdUtils.norm_all_col( full_train_set_pd, norm_sch_id = 1 )

        kmeans = KMeans(n_clusters=4)
        kmeans.fit(full_train_set_pd)

        # Obtain the labels applied to the fitting data.
        y = kmeans.labels_
        
        y_gr1 = y[range( len( gr1_fdc_id ) )]
        y_gr2 = y[range( len( gr1_fdc_id ), len( gr1_fdc_id ) + len( gr2_fdc_id ) )]
        print( y_gr1 )
        print( y_gr2 )




class ML_5fdGr_res:
    '''
    This class is simply a way to easily access various key data from the 
    simulation results obtained after running a ML process from the "ML_5fdGr" class.
    '''

    def __init__( self, model, ML_setup, full_eval_res ):
        
        self.model = model
        self.ML_setup = ML_setup
        self.full_eval_res = full_eval_res


    def get_acc( self ):
        return self.full_eval_res["accuracy"]
    def get_acc_gr1( self ):
        return self.full_eval_res["accuracy_gr1"]
    def get_acc_gr2( self ):
        return self.full_eval_res["accuracy_gr2"]
    def get_test_gr1_nut( self ):
        return self.full_eval_res["test_gr1_nut"]
    def get_test_gr2_nut( self ):
        return self.full_eval_res["test_gr2_nut"]
    def get_pred_right( self ):
        return self.full_eval_res["pred_right"]

    def get_gr1_name( self ):
        return self.ML_setup["gr1_name"]
    def get_gr2_name( self ):
        return self.ML_setup["gr2_name"]

    def get_train_gr1_id( self ):
        return self.ML_setup["train_gr1_id"]
    def get_train_gr2_id( self ):
        return self.ML_setup["train_gr2_id"]
    def get_train_gr1_nut( self ):
        return self.ML_setup["train_gr1_nut"]
    def get_train_gr2_nut( self ):
        return self.ML_setup["train_gr2_nut"]
    def get_test_gr1_id( self ):
        return self.ML_setup["test_gr1_id"]
    def get_test_gr2_id( self ):
        return self.ML_setup["test_gr2_id"]
    
