


import pandas as pd
import numpy as np


def norm_all_col( df_orig, **args ):
    '''
    Normalize the data entries columnwise.
    You better make sure your dataFrame values are ALL numerical.

    Extra arguments:
    
    [norm_sch_id]
        0: min-max normalization
        1: mean normalization
    '''

    # Set the normalization scheme ID.
    if "norm_sch_id" in args:
        norm_sch_id = args["norm_sch_id"]
    else:
        norm_sch_id = 0

    df_shape = df_orig.shape
    df_norm_series_list = [None]*df_shape[1]
    
    # min-max normalization.
    if norm_sch_id == 0:
        
        # Performing normalization column by column.
        for z in range( df_shape[1] ):
            
            # Obtain the current column and compute min-max ops.
            df_z = df_orig.iloc[:,z]
            tmp1 = df_z - df_z.min()
            tmp2 = df_z.max()-df_z.min()

            # If min == max, simply set all entries to 1.
            if tmp2 == 0:
                # If all column entries are the same, hard set to 1 for all.
                if df_z.max() != 0:
                    tmp = df_z/df_z.max()
                # Do nothing if all column entries are zero.
                else:
                    tmp = df_z
            # Normalize using max to min distance.
            else:
                tmp = tmp1/tmp2

            df_norm_series_list[z] = tmp

        df_norm = pd.DataFrame( df_norm_series_list )
        df_norm = df_norm.transpose()

    # Mean normalization.
    elif norm_sch_id == 1:

        # Performing normalization column by column.
        for z in range( df_shape[1] ):
            
            # Obtain the current column and compute min-max ops.
            df_z = df_orig.iloc[:,z]
            tmp1 = df_z - df_z.mean()
            tmp2 = df_z.std()
            
            # If min == max, simply set all entries to 1.
            if tmp2 == 0:
                # If all column entries are the same, hard set to 1 for all.
                if not ( df_z.max() == 0 and df_z.min() == 0 ):
                    tmp = df_z/df_z.max()
                # Do nothing if all column entries are zero.
                else:
                    tmp = df_z
            # Normalize using max to min distance.
            else:
                tmp = tmp1/tmp2

            df_norm_series_list[z] = tmp

        df_norm = pd.DataFrame( df_norm_series_list )
        df_norm = df_norm.transpose()

    return df_norm

def sub_df_at_col( df_orig, col_name, tar_val ):
    '''
    Obtain a sub-dataframe from the given data frame "df_orig" whose column 
    by the name "col_name" contains the target value "tar_val".

    The returned sub-dataframe is going to be ordered based on the order of 
    values specified in "tar_val".
    '''
    
    df_sub = df_orig.loc[df_orig[col_name].isin(tar_val)].copy(deep=True)
    # Set 'col_name' as a categorical with the specified order
    df_sub[col_name] = pd.Categorical(df_sub[col_name], categories=tar_val, ordered=True)
    # Sort by this categorical column to respect order
    df_sub = df_sub.sort_values(col_name)

    return df_sub


def get_idx_of( df_orig, col_name, tar_val ):
    '''
    Return the indices of entries in "df_orig" whose value at
    column "col_name" matches the value(s) in tar_val.

    Note that if "tar_val" contains multiple values, the returning NumPy 
    array of row indices DO NOT DIFFERENTIATE which detected indices are matched 
    due to which value in "tar_val".
    The returned index array is simply the cumulation of all matches.
    '''

    #tar_idx_arr = df_orig.index[df_orig[col_name] == tar_val].to_numpy()

    match_bool_arr = df_orig[col_name].isin(tar_val)
    row_idx = df_orig.index[match_bool_arr]

    return row_idx
