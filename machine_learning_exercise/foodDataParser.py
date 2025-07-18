

import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )

import re
import pandas as pd
import numpy as np
from toolbox import pandasUtils as pdUtil

class foodDataParser:
    '''
    This class is expected to be defined at a directory where the 'food_data' 
    directory is located.
    '''

    # The name of the directory where the food database csv files are located.
    dirname = os.path.dirname(__file__)

    file_food = f"{dirname}\\food_data\\food.csv"
    file_food_portion = f"{dirname}\\food_data\\food_portion.csv"
    file_food_nutrient = f"{dirname}\\food_data\\food_nutrient.csv"
    file_nutrient = f"{dirname}\\food_data\\nutrient.csv"
    file_food_category = f"{dirname}\\food_data\\food_category.csv"
    file_foundation_food = f"{dirname}\\food_data\\foundation_food.csv"

    # The dataframe of the 'food' file.
    df_food = pd.read_csv( file_food )
    # The dataframe of the 'food_portion' file.
    df_food_portion = pd.read_csv( file_food_portion )
    # The dataframe of the 'food_nutrient' file.
    df_food_nutrient = pd.read_csv( file_food_nutrient, low_memory=False )
    # The dataframe of the 'food_nutrient' file.
    df_nutrient = pd.read_csv( file_nutrient )
    # The dataframe of the 'file_food_category' file.
    df_food_category = pd.read_csv( file_food_category )

    # The dataframe of the 'foundation_food' file
    df_found_food = pd.read_csv( file_foundation_food )

    def __init__(self):

        # The id of the last food item being searched for.
        self.currFoodID = -1

    def __str__(self):
        

        str_ans = "Food database parser based on database located at"
        str_ans = f"{str_ans}\n   {foodDataParser.dirname}"
        str_ans = f"{str_ans}\n   Current food ID: {self.currFoodID}"
        return str_ans
  

    def findFood_byIdx( self, food_ID ):
        '''
        Determine the base food info using the fdc_id of the food, a unique
        identification number to all food items of the database.
        This function resets the current food ID.
        '''

        df = foodDataParser.df_food

        # Obtain array of food indices (fdc_id). 
        # There should be a unique match or no match.
        tarFood_idx = df.index[df['fdc_id'] == food_ID].tolist()

        # Obtain the base info of the target food item.
        tarFood_info = df.loc[tarFood_idx]

        # Update the current food ID.
        self.currFoodID = food_ID

        # Return base info.
        return tarFood_info

    def getAllFoundFood(self):
        '''
        Return the list of all foundation foods.
        Each entry in the list is a tuple containing the food ID and the 
        name of a foundational food.
        '''
        
        # dropping null value columns to avoid errors
        # self.df_found_food.dropna(inplace = True)

        fnd_fd_id_arr = self.df_found_food[ "fdc_id" ].to_numpy()

        fnd_fd_idx_arr = pdUtil.get_idx_of( self.df_food, "fdc_id", fnd_fd_id_arr ).to_numpy()

        fd_name_arr = self.df_food[ "description" ].to_numpy()
        fnd_fd_name_arr = fd_name_arr[ fnd_fd_idx_arr ]

        # Create the tuple array using numpy's 'object' dtype
        tuple_array = np.empty(fnd_fd_id_arr.shape, dtype=object)

        # Populate the tuple array
        for i in range(fnd_fd_id_arr.size):  # Or numbers.shape[0]  if you want to be more explicit
            tuple_array[i] = (fnd_fd_id_arr[i], fnd_fd_name_arr[i])

        return tuple_array


    def findFoundFood(self, keyword):
        '''
        Determines the row index of the target foundation food containing
        the given keyword. 
        For example, one can find the foundation food 'broccoli, raw' using
        the keyword 'broccoli'.
        '''

        # Use the 'food' document dataframe.
        df_food = foodDataParser.df_food

        # dropping null value columns to avoid errors
        df_food.dropna(inplace = True)

        # Determine where the keyword appears in the description of food items.
        keyword_mod = f'{keyword}'
        keyword_bool = df_food["description"].str.contains(keyword_mod, case=False, regex=True)
        # Determine where are the foundation food defined.
        found_bool = df_food["data_type"].str.contains("foundation_food", case=False)

        # Determine where we have both the keyword matching as well as the food type
        # begin a foundation food.
        match_row_idx = np.logical_and(keyword_bool, found_bool)

        return df_food.loc[match_row_idx]



    def find_fd_gr_preset_nut( self, fdc_id_arr, **args ):
        '''
        Specialized function which returns the nutrient amounts of select 
        food items in a NumPy array.

        Uses presets from the "food" class for selecting the nutrients info to
        extract.

        The food group nutrient data is given without name of the food or nutrients.
        This format is deliberate to facilitate use of nutrient data for
        Machine Learning purposes.
        '''

        # Set the food nutrient information list format.
        if "nut_format_id" in args:
            nut_format_id = args["nut_format_id"]
        else:
            nut_format_id = 0
        
        # Obtain the number of food items to look for.
        fd_cnt = len( fdc_id_arr )
        # Initialize the food group nutrient array.
        food_gr_nut_arr = []
        
        for z in range( fd_cnt ):

            # Obtain a 'food' object of the target food ID.
            fdc_id_z = fdc_id_arr[z]
            food_z = self.findFood_nutrients( fdc_id = fdc_id_z )

            # Obtain the nutrient information of the food under the desired format.
            food_z_nut = food_z.get_preset_nut( nut_format_id )

            # Obtain the nutrients in a np array.
            food_z_nut_np = food_z_nut['nut_amt'].to_numpy()

            # Stack the nutrients of the current food unto the food group nutrient array.
            if len(food_gr_nut_arr) == 0:
                food_gr_nut_arr = food_z_nut_np
            else:
                food_gr_nut_arr = np.vstack( ( food_gr_nut_arr, food_z_nut_np ) )

        return food_gr_nut_arr
        

    def find_fd_gr_nut( self, fdc_id_arr, **args ):
        '''
        Specialized function which returns the nutrient amounts of select 
        food items in a NumPy array.

        Use user defined set of nutrient IDs to extract target nutrients.
        Nutrient IDs should come as a list or an array of integers.

        The food group nutrient data is given without name of the food or nutrients.
        This format is deliberate to facilitate use of nutrient data for
        Machine Learning purposes.
        '''

        # Set the food nutrient information list format.
        if "nut_id_list" in args:
            nut_id_list = args["nut_id_list"]
        else:
            nut_id_list = food.get_preset_nut_id(0)
        
        # Obtain the number of food items to look for.
        fd_cnt = len( fdc_id_arr )
        # Initialize the food group nutrient array.
        food_gr_nut_arr = []
        
        for z in range( fd_cnt ):

            # Obtain a 'food' object of the target food ID.
            fdc_id_z = fdc_id_arr[z]
            food_z = self.findFood_nutrients( fdc_id = fdc_id_z )

            # Obtain the nutrient information of the food under the desired format.
            food_z_nut = food_z.get_nutrients( nut_id_list = nut_id_list )

            # Obtain the nutrients in a np array.
            food_z_nut_np = food_z_nut['nut_amt'].to_numpy()

            # Stack the nutrients of the current food unto the food group nutrient array.
            if len(food_gr_nut_arr) == 0:
                food_gr_nut_arr = food_z_nut_np
            else:
                food_gr_nut_arr = np.vstack( ( food_gr_nut_arr, food_z_nut_np ) )

        return food_gr_nut_arr



    def findFood_nutrients( self, **args ):
        '''
        Determines the nutrients of the target food item.
        args[0] = fdc_id of the target food item

        If no input argument, use the 'currFoodID' found 
        by calling a search function of this class.
        '''

        # Set the search ID according to whether an ID is given or not.
        if "fdc_id" in args:
            tar_fdc_id = args["fdc_id"]
        else:
            return "Cannot search for food nutrient without target food ID: 'fdc_id'."


        # Use the 'food_nutrients' document dataframe.
        df_food_nut = foodDataParser.df_food_nutrient
        # Use the 'nutrient' document dataframe.
        df_nut = foodDataParser.df_nutrient
        # Obtain the list of nutrient IDs (fdc_id) that are official in the 'food' class.
        official_nut_id = food.df_nut_id_map['nutrient_id'].to_numpy()

        # Obtain the list of nutrient information related to the target food only.
        tar_idx_arr = pdUtil.get_idx_of( df_food_nut, 'fdc_id', [tar_fdc_id] )
        tar_nut_id = df_food_nut['nutrient_id'][tar_idx_arr].to_numpy()

        # Retain nutrient IDs that are also in the 'food' class official list.
        tar_offic_nut_id = \
            list( set( tar_nut_id ).intersection( official_nut_id ) )
        # Make sure the array is in ascending order.
        tar_offic_nut_id.sort()

        # Create sub-dataframe from the dataframe df_nut which only retains nutrient
        # information of the target food AND recognized by the 'food' class.
        df_tar_nut = pdUtil.sub_df_at_col( df_nut, 'id', tar_offic_nut_id )
        # Sort the fd_nut sub-dataframe in ascending order of nutrient IDs.
        df_tar_nut.sort_values( by=['id'], inplace = True )
        
        # Create sub-dataframe from the dataframe df_food_nut which only retains nutrient
        # information of the target food AND recognized by the 'food' class.
        tmp_df = df_food_nut.loc[tar_idx_arr]      
        df_tar_fd_food_nut = pdUtil.sub_df_at_col( tmp_df, 'nutrient_id', tar_offic_nut_id )
        # Sort the df_food_nut sub-dataframe in ascending order of nutrient IDs.
        df_tar_fd_food_nut.sort_values( by=['nutrient_id'], inplace = True )
        

        filt_nut_id_list = np.array( tar_offic_nut_id )
        filt_amt_list = df_tar_fd_food_nut['amount'].to_numpy()
        filt_nut_unit_list = df_tar_nut['unit_name'].to_numpy()
        

        # Create the target food object.
        tarFood = food( tar_fdc_id )
        # In this database, default food sample size used to measure the nutrients 
        # is 100 gram.
        tarFood.food_unit = 'G'
        tarFood.food_amt = 100

        # Create a reference copy of the nutrient dataframe of the food object.
        fd_obj_df_nut = tarFood.df_nut.copy(deep = False)
        

        for z in range( len( fd_obj_df_nut['nutrient_id'] ) ):
            
            # Determine if the current food nutrient exists in the official list of
            # nutrients for the current food.
            x = np.where(filt_nut_id_list == fd_obj_df_nut['nutrient_id'][z] )

            # Index unpacking.
            match_idx = x[0]
            # Check for void case.
            if len(match_idx) != 0:
                match_idx = match_idx[0]
                fd_obj_df_nut.loc[z, 'nut_amt'] = filt_amt_list[match_idx]
                fd_obj_df_nut.loc[z, 'nut_unit'] = filt_nut_unit_list[match_idx]
            #print( f"{fd_obj_df_nut['nutrient_id'][z]} {match_idx}", end = ", " )

        return tarFood
    

    def getNutrName( self, nut_id ):

        # Use the 'nutrient' document dataframe.
        df_nut = foodDataParser.df_nutrient

        if isinstance(nut_id, list):
            df_tar_nut = pdUtil.sub_df_at_col( df_nut, 'id', nut_id )
        elif isinstance( nut_id, (int, float, np.number) ):
            df_tar_nut = pdUtil.sub_df_at_col( df_nut, 'id', [nut_id] )
        else:
            print( "Wrong input given to getNutrName" )
            return

        return df_tar_nut['name'].to_numpy()
    

    def getNutrUnit( self, nut_id ):

        # Use the 'nutrient' document dataframe.
        df_nut = foodDataParser.df_nutrient

        if isinstance(nut_id, list):
            df_tar_nut = pdUtil.sub_df_at_col( df_nut, 'id', nut_id )
        elif isinstance( nut_id, (int, float, np.number) ):
            df_tar_nut = pdUtil.sub_df_at_col( df_nut, 'id', [nut_id] )
        else:
            print( "Wrong input given to getNutrName" )
            return

        return df_tar_nut['unit_name'].to_numpy()





        




class food:
    '''
    A food object must contain:
    > ID: We borrow the fdc_id used by the database as the ID of the food objects.
    > Name: We will use the same name used in the database.
    > Category and category ID: Again, use the same as the one in the database.
    > Nutrients: A select key nutrients will be added to the food item. 
        The key nutrients are defined in a supporting csv document under the name
            "key_nutrient_id_map.csv"
    '''

    # Define the utility subdirectory for this class
    util_dir = f"{os.path.dirname(__file__)}/foodDataParser_util"

    # Obtain the dataframe of nutritients that are recognized by this class.
    # df_nut_id_map = pd.read_csv( f"{util_dir}\\key_nutrient_id_map.csv" )
    df_nut_id_map = pd.read_csv( f"{util_dir}\\full_nutrient_id_map.csv" )
    # Define the name of the sub-directory where the food objects are to be saved.
    data_subdir = "food_nut_csv"

    def __init__( self, fdc_id ):

        # Obtain the current file's path.
        dirname = os.path.dirname(__file__)

        # Obtain the list of nutrient names.
        nut_name_list = food.df_nut_id_map['name'].tolist()
        # Obtain the list of nutrient IDs (fdc_id).
        nut_id_list = food.df_nut_id_map['nutrient_id'].tolist()
        # Generate an array of all zeros as initial amount of all nutrients.
        init_amt_val_arr = np.zeros( len( nut_id_list ) )
        # Generate an array of 
        init_unit_arr = [None] * len( nut_id_list )
        

        # Define dictionary that is to be used for dataframe.
        data = {
            "nutrient_id": nut_id_list,
            "nut_name_list": nut_name_list,
            "nut_amt": init_amt_val_arr,
            "nut_unit": init_unit_arr
        }
        # load data into a DataFrame object:
        df_nut = pd.DataFrame(data)



        df_food = foodDataParser.df_food
        # Obtain the string description (name) of the target food.
        tar_name_idx = pdUtil.get_idx_of( df_food, 'fdc_id', [fdc_id] )
        tar_name = df_food.loc[tar_name_idx]['description']
        tar_name = tar_name.values[0]

        

        df_food_cat = foodDataParser.df_food_category
        # Obtain the ID of the food category to which the target food belongs.
        tar_cat_id = df_food.loc[tar_name_idx]['food_category_id']
        tar_cat_id = tar_cat_id.values[0]
        # Obtain the name of the food category.
        # tar_cat_idx = df_food_cat.index[ df_food_cat['id'] == tar_cat_id ].tolist()
        tar_cat_idx = pdUtil.get_idx_of( df_food_cat, 'id', [tar_cat_id] )
        tar_cat_name = df_food_cat.loc[tar_cat_idx]['description']
        tar_cat_name = tar_cat_name.values[0]


        self.fdc_id = fdc_id
        self.name = tar_name
        self.category_id = tar_cat_id
        self.category_name = tar_cat_name
        self.df_nut = df_nut
        # Set the default amount of food.
        self.food_amt = 100
        # Set the default food amount unit to gram.
        self.food_unit = 'G'
    

    def __str__( self, *args ):
              
        # Set the flag for printing the nutritient facts (default is do not print).
        if len( args ) == 1:
            do_nut = args[0]
        else:
            do_nut = False

        # Print the information of the current food.
        str_ans = "Food information:"
        str_ans = f"{str_ans}\n   Food name: {self.name} (ID/fdc_id: {self.fdc_id})"
        str_ans = f"{str_ans}\n   Food category: {self.category_name} (ID: {self.category_id})"
        if do_nut:
            str_ans = f"{str_ans}\n   Food nutritient dataframe:\n{self.df_nut}"

        return str_ans
    

    def write_to_file( self, **args ):
        
        # Set the format ID.
        if "format_id" in args:
            format_id = args["format_id"]
        else:
            format_id = 0

        # The file name is based on the name of the food.
        file_name = self.name
        # Replace everything except words with underscore in the food name.
        file_name = re.sub( r'[^\w]','_', file_name ) 

        # Obtain the current file's path.
        path = os.path.dirname(__file__)
        # Attach the sub-directory name.
        path_mod = path + "\\" + food.data_subdir
        # Create the sub-directory if not present.
        if not os.path.exists( path_mod ):
            os.mkdir( path_mod )


        # Complete the full file name.
        path_mod = path_mod + "\\" + file_name + ".csv"

        # Obtain the nutrients dataframe.
        df_nut = self.get_preset_nut( format_id )
        # Print the nutrient dataframe of the present food to the csv file.
        df_nut.to_csv( path_or_buf = path_mod, sep = ',' )

    @staticmethod
    def get_preset_nut_id( preset_id ):
        '''
        Preset lists of nutrients IDs can be fetched by this function once
        the desired present's ID "preset_id" is given.

        Each preset list can be used to extract a subset of the full nutrient
        dataFrame where only nutrients whose IDs appear in the preset list remain.
        '''

        if preset_id == -1:

            # Obtain the dataframe of nutritients that are recognized by this class.
            df_nut_id_map_tmp = pd.read_csv( f"{food.util_dir}\\full_nutrient_id_map.csv" )
            nut_id_arr = np.array( df_nut_id_map_tmp['nutrient_id'] )

        if preset_id == 0:

            nut_id_arr = np.array( food.df_nut_id_map['nutrient_id'] )
            # nut_id_arr = food.df_nut_id_map['nutrient_id']

        # Slightly reduced nutrient map. Cut some minerals and vitamins.
        elif preset_id == 1:
            
            # nut_id_arr = np.array( [1051, 1085, 1258, 1257, 1253, 1093, \
            #         1005, 1079, 1063, 1003, 1106, 1162, 1114, \
            #         1109, 1183, 1184, 1185, 1165, 1166, 1167, \
            #         1170, 1175, 1176, 1177, 1178, 1087, 1091, \
            #         1092, 1088, 1090, 1089 ] )

            # Obtain the dataframe of nutritients that are recognized by this class.
            df_nut_id_map_tmp = pd.read_csv( f"{food.util_dir}\\sub_nutrient_id_map_format_1.csv" )
            nut_id_arr = np.array( df_nut_id_map_tmp['nutrient_id'] )
            
        # No vitamins or minerals.
        elif preset_id == 2:
        
            # nut_id_arr = np.array( [1051, 1085, 1258, 1257, 1253, 1093, \
            #         1005, 1079, 1063, 1003 ] )
            
            # Obtain the dataframe of nutritients that are recognized by this class.
            df_nut_id_map_tmp = pd.read_csv( f"{food.util_dir}\\sub_nutrient_id_map_format_2.csv" )
            nut_id_arr = np.array( df_nut_id_map_tmp['nutrient_id'] )
        
        # Specialized and depends on when I last edited ...
        elif preset_id == 3:

            # nut_id_arr = np.array( [1085, 1257, 1253, 1005, 1079, 1003 ] )

            # Obtain the dataframe of nutritients that are recognized by this class.
            df_nut_id_map_tmp = pd.read_csv( f"{food.util_dir}\\sub_nutrient_id_map_format_3.csv" )
            nut_id_arr = np.array( df_nut_id_map_tmp['nutrient_id'] )

        # Specialized nutrient list that are useful for food group identification
        # through neural network.
        elif preset_id == 4:
        
            # nut_id_arr = np.array( [ 1258, 1292, 1293, 1257, 1253, \
            #     1106, 1162, 1114, 1183, 1185, \
            #     1178, 1100, 1094, 1097, 1098, 1101, 1103, \
            #     1093, 1079, 1002, 1003, 1176, 1089 ] )

            # Obtain the dataframe of nutritients that are recognized by this class.
            df_nut_id_map_tmp = pd.read_csv( f"{food.util_dir}\\sub_nutrient_id_map_format_4.csv" )
            nut_id_arr = np.array( df_nut_id_map_tmp['nutrient_id'] )

        return nut_id_arr


    def get_preset_nut( self, preset_id ):
        '''
        Obtain the nutrients of the present food instance using a preset
        format where only a select number of nutrients are taken.

        Look at function get_nut_preset() from this class to see exactly 
        how the presets are defined.
        '''

        # Obtain the preset list of nutrient IDs.
        pres_nut_id_arr = food.get_preset_nut_id( preset_id )
        # Use the preset nutrient ID list to extract a subset of the full
        # nutrient dataframe.
        df_tmp = pdUtil.sub_df_at_col( self.df_nut, 'nutrient_id', pres_nut_id_arr )
        # Reset the sub-dataframe indexing.
        df_tmp = df_tmp.reset_index(drop = True)

        return df_tmp


    def get_nutrients( self, **args ):
        '''
        Obtain the nutrients of the present food instance.

        '''

        # Set the format ID.
        if "nut_id_list" in args:
            nut_id_list = args["nut_id_list"]
        else:
            return self.df_nut

        sub_df_nut = pdUtil.sub_df_at_col( self.df_nut, 'nutrient_id', nut_id_list )
        sub_df_nut = sub_df_nut.reset_index(drop = True)
        return sub_df_nut

    


            
        

        




    






