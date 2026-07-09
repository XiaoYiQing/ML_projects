

import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt



from plot_funcs import Lin3SegmConfig
from plot_funcs import gen_Lin3SegmPlotData
from plot_funcs import LogisticFuncConfig
from plot_funcs import fit_logistic_2_pts
from plot_funcs import get_logistic_plot_data


# ======================================================================= >>>>>
#       General
# ======================================================================= >>>>>

class randDGen_Lin3Segm:
    '''
    A class that holds the range of possible control variables for the specific
    plot function Lin3Segm which consists of three segments of linear functions
    attached together in a continuous fashion where the middle segment is a 
    significant drop.

    The class also holds a function that generate this function's plot data in
    a randomized fashion according to the defined range of possible control 
    variables.
    '''

    def __init__(self, ref_x = (0,1), drop_mid_pt_rng = ( 0.10, 0.90 ), drop_width_rng = ( 0.02, 0.12 ), y_max_rng = ( 0.90, 0.95 ), y_min_rng = ( 0.05, 0.10 ), y_pre_drop_dip_rng = ( 0.01, 0.05 ), y_post_drop_dip_rng = ( 0.01, 0.05 ), x_arr = np.linspace(0,1,101) ):
        
        
        # The two reference x points. These are not x-limits, but just the x two points
        # with which the function is defined with.
        self.ref_x = ref_x
        # The steep linear drop segment's midpoint range.
        self.drop_mid_pt_rng = drop_mid_pt_rng
        # The steep linear drop segment's width range.
        self.drop_width_rng = drop_width_rng
        # The range of y starting value (highest point, at smallest x)
        self.y_max_rng = y_max_rng
        # The range of y ending value (lowerst point, at highest x)
        self.y_min_rng = y_min_rng
        
        # The slight dip in y from its highest point to the point where the main drop starts.
        self.y_pre_drop_dip_rng = y_pre_drop_dip_rng
        # The slight dip in y from where the main drop ends to the lowest y value.
        self.y_post_drop_dip_rng = y_post_drop_dip_rng

        # The x array where the function is to be evaluated.
        self.x_arr = x_arr
        

    def gen_data( self, n : int ):
        '''
        Generate randomized plot data sets according to the current class instance's
        specified allowed randomization ranges.

        Args:
            n: The number of random data set cases.
        '''

        # Generate the randomized parameters for the three segments linear plot.
        drop_mid_pt_arr = np.random.uniform( self.drop_mid_pt_rng[0], self.drop_mid_pt_rng[1], size = n )
        drop_width_arr = np.random.uniform( self.drop_width_rng[0], self.drop_width_rng[1], size = n )
        y_max_arr = np.random.uniform( self.y_max_rng[0], self.y_max_rng[1], size = n )
        y_min_arr = np.random.uniform( self.y_min_rng[0], self.y_min_rng[1], size = n )
        y_pre_drop_dip_arr = np.random.uniform( self.y_pre_drop_dip_rng[0], self.y_pre_drop_dip_rng[1], size = n )
        y_post_drop_dip_arr = np.random.uniform( self.y_post_drop_dip_rng[0], self.y_post_drop_dip_rng[1], size = n )

        data_pt_cnt = len( self.x_arr )
        # The array to store the data.
        Y = np.zeros( ( n, data_pt_cnt ) )
        config_arr = [Lin3SegmConfig() for _ in range(n)]

        # Create the linear drop plot data given the specified randomization parameters.
        for z in range(n):

            myConfig_z = Lin3SegmConfig()
            myConfig_z.x1 = self.ref_x[0]
            myConfig_z.y1 = y_max_arr[z]
            myConfig_z.x2 = drop_mid_pt_arr[z] - drop_width_arr[z]/2
            myConfig_z.y2 = y_max_arr[z] - y_pre_drop_dip_arr[z]
            myConfig_z.x3 = drop_mid_pt_arr[z] + drop_width_arr[z]/2
            myConfig_z.y3 = y_min_arr[z] + y_post_drop_dip_arr[z]
            myConfig_z.x4 = self.ref_x[1]
            myConfig_z.y4 = y_min_arr[z]

            y_arr_z = gen_Lin3SegmPlotData( myConfig_z, self.x_arr )

            Y[z,:] = y_arr_z[:]
            config_arr[z] = myConfig_z

        return Y, config_arr

    # def to_str(self):
    #     return f"MyClass(name={self.name}, x={self.x}, y={self.y})"



'''
# The absolute x limit to the drop's defining points.
x_drop_rng_lim = ( 0.02, 0.98 )

# The range of mid points allowed.
drop_mid_pt_rng = ( 0.20, 0.80 )
# The range of width the logistic drop is allowed.
drop_width_rng = ( 0.10, 0.40 )

# The range of y starting value (highest point)
y_max_rng = ( 0.95, 1.00 )
# The range of y ending value (lowest point)
y_min_rng = ( 0.00, 0.05 )

# The slight dip in y from its highest point to the point where the main drop occurs.
y_pre_drop_dip_rng = ( 0.01, 0.05 )
# The slight dip in y from where the main drop ends to the lowest y value.
y_post_drop_dip_rng = ( 0.01, 0.05 )
'''

class randDGen_logistic:

    def __init__( self, x_drop_rng_lim = ( 0.02, 0.98 ), drop_mid_pt_rng = ( 0.20, 0.80 ), drop_width_rng = ( 0.10, 0.40 ), \
        y_max_rng = ( 0.95, 1.00 ), y_min_rng = ( 0.00, 0.05 ), y_pre_drop_dip_rng = ( 0.01, 0.05 ), \
        y_post_drop_dip_rng = ( 0.01, 0.05 ), x_arr = np.linspace(0,1,101) ):

        # The absolute x limit to the drop's defining points (The x points where the drop starts/ends 
        # cannot go over this range).
        self.x_drop_rng_lim = x_drop_rng_lim
        # The range of mid points allowed.
        self.drop_mid_pt_rng = drop_mid_pt_rng
        # The range of width the logistic drop is allowed (How wide is the drop, approximately).
        self.drop_width_rng = drop_width_rng
        # The range of y starting value (logistic function upper limit).
        self.y_max_rng = y_max_rng
        # The range of y ending value (logistic function lower limit).
        self.y_min_rng = y_min_rng
        # The slight dip in y from its highest point to the point where the main drop occurs.
        self.y_pre_drop_dip_rng = y_pre_drop_dip_rng
        # The slight dip in y from where the main drop ends to the lowest y value.
        self.y_post_drop_dip_rng = y_post_drop_dip_rng
        # The x array where the function is to be evaluated.
        self.x_arr = x_arr

    def gen_data( self, n : int ):

        # Generate the randomized parameters for the three segments linear plot.
        drop_mid_pt_arr = np.random.uniform( self.drop_mid_pt_rng[0], self.drop_mid_pt_rng[1], size = n )
        drop_width_arr = np.random.uniform( self.drop_width_rng[0], self.drop_width_rng[1], size = n )
        y_max_arr = np.random.uniform( self.y_max_rng[0], self.y_max_rng[1], size = n )
        y_min_arr = np.random.uniform( self.y_min_rng[0], self.y_min_rng[1], size = n )
        y_pre_drop_dip_arr = np.random.uniform( self.y_pre_drop_dip_rng[0], self.y_pre_drop_dip_rng[1], size = n )
        y_post_drop_dip_arr = np.random.uniform( self.y_post_drop_dip_rng[0], self.y_post_drop_dip_rng[1], size = n )

        data_pt_cnt = len( self.x_arr )
        # The array to store the data.
        Y = np.zeros( ( n, data_pt_cnt ) )
        config_arr = [LogisticFuncConfig() for _ in range(n)]

        # Create the logistic plot data given the specified randomization parameters.
        for z in range(n):

            y_min_z = y_min_arr[z]
            y_max_z = y_max_arr[z]
            drop_mid_pt_z = drop_mid_pt_arr[z]
            drop_width_z = drop_width_arr[z]
            y_pre_drop_dip_z = y_pre_drop_dip_arr[z]
            y_post_drop_dip_z = y_post_drop_dip_arr[z]

            x_a = drop_mid_pt_z - drop_width_z/2.0
            x_a = max( x_a, self.x_drop_rng_lim[0] )
            x_b = drop_mid_pt_z + drop_width_z/2.0
            x_b = min( x_b, self.x_drop_rng_lim[1] )
            y_a = y_max_z - y_pre_drop_dip_z
            y_b = y_min_z + y_post_drop_dip_z

            myConfig_z = fit_logistic_2_pts( x_a, y_a, x_b, y_b, y_min_z, y_max_z )

            y_arr_z = get_logistic_plot_data( myConfig_z, self.x_arr )

            Y[z,:] = y_arr_z[:]
            config_arr[z] = myConfig_z


        return Y, config_arr

# ======================================================================= <<<<<

