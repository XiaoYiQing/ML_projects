

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
from plot_funcs import LogisticFuncConfig
from plot_funcs import PolyDropFuncConfig
from plot_funcs import gen_Lin3SegmPlotData
from plot_funcs import fit_logistic_2_pts
from plot_funcs import get_logistic_plot_data
from plot_funcs import gen_linPolyLin_plotData


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

    def __init__(self, ref_x = (0,1), drop_mid_pt_rng = ( 0.10, 0.90 ), \
        drop_width_rng = ( 0.02, 0.12 ), y_max_rng = ( 0.90, 0.95 ), \
        y_min_rng = ( 0.05, 0.10 ), y_pre_drop_dip_rng = ( 0.01, 0.05 ), \
        y_post_drop_dip_rng = ( 0.01, 0.05 ) ):
        
        
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


    def gen_data( self, n : int, x_arr ):
        '''
        Generate randomized plot data sets according to the current class instance's
        specified allowed randomization ranges.

        Args:
            n: The number of random data set cases.
        '''

        data_pt_cnt = len( x_arr )
        if data_pt_cnt == 0:
            return False, False, False
        
        # Generate the randomized parameters for the three segments linear plot.
        drop_mid_pt_arr = np.random.uniform( self.drop_mid_pt_rng[0], self.drop_mid_pt_rng[1], size = n )
        drop_width_arr = np.random.uniform( self.drop_width_rng[0], self.drop_width_rng[1], size = n )
        y_max_arr = np.random.uniform( self.y_max_rng[0], self.y_max_rng[1], size = n )
        y_min_arr = np.random.uniform( self.y_min_rng[0], self.y_min_rng[1], size = n )
        y_pre_drop_dip_arr = np.random.uniform( self.y_pre_drop_dip_rng[0], self.y_pre_drop_dip_rng[1], size = n )
        y_post_drop_dip_arr = np.random.uniform( self.y_post_drop_dip_rng[0], self.y_post_drop_dip_rng[1], size = n )

        # The array to store the data.
        Y = np.zeros( ( n, data_pt_cnt ) )
        config_arr = [Lin3SegmConfig() for _ in range(n)]

        # Create the linear drop plot data given the specified randomization parameters.
        for z in range(n):

            config_arr[z].x1 = self.ref_x[0]
            config_arr[z].y1 = y_max_arr[z]
            config_arr[z].x2 = drop_mid_pt_arr[z] - drop_width_arr[z]/2
            config_arr[z].y2 = y_max_arr[z] - y_pre_drop_dip_arr[z]
            config_arr[z].x3 = drop_mid_pt_arr[z] + drop_width_arr[z]/2
            config_arr[z].y3 = y_min_arr[z] + y_post_drop_dip_arr[z]
            config_arr[z].x4 = self.ref_x[1]
            config_arr[z].y4 = y_min_arr[z]

            y_arr_z = gen_Lin3SegmPlotData( config_arr[z], x_arr )

            Y[z,:] = y_arr_z[:]

        return Y, config_arr

    # def to_str(self):
    #     return f"MyClass(name={self.name}, x={self.x}, y={self.y})"




class randDGen_logistic:
    '''
    A class that holds the range of possible control variables for a logistic 
    function. This logistic function has a upper and lower limits that it approaches 
    asymptomatically, but the area of interest is the portion where it transitions
    from one asymptote to the other. The logistic function is designed to have a
    descending profile, but does not prevent an ascending one, though some unexpected
    behavior may occur.

    Randomized data generation based on this logistic function will be under the range 
    of control parameters within this class.

    Attributes
    ----------
    x_drop_rng_lim : ( float, float )
        The lower and upper bounds on the x-axis where the reference points used to define
        the logistic function is allowed to be situated.
    drop_mid_pt_rng : ( float, float )
        The range of x-values where the mid-point of the transitional portion of the 
        logistic function can be randomly located.
    drop_width_rng : ( float, float )
        The range of width of the transition portion of the function that can be randomly
        selected.
        NOTE: This is not the actual width of transition segment, but rather the locator
        for the x-values of two reference points (x_a,y_a) and (x_b,y_b) located equal 
        distance from the mid-point (one below and one above). These two reference points 
        are what decides the true parameters of the logistic function.
    y_max_rng : ( float, float )
        The range of possible randomly selected upper y-asymptote.
    y_max_rng : ( float, float )
        The range of possible randomly selected lower y-asymptote.
    y_pre_drop_dip_rng : ( float, float )
        The range of values of y_max - y_a (The amount shaved from the upper limit to reach
        the first reference point (x_a,y_a) ).
    y_post_drop_dip_rng : ( float, float )
        The range of values of y_b - y_min (The amount added to the lower limit to reach
        the second reference point (x_b,y_b) ).
    '''

    def __init__( self, x_drop_rng_lim = ( 0.02, 0.98 ), drop_mid_pt_rng = ( 0.20, 0.80 ), drop_width_rng = ( 0.10, 0.40 ), \
        y_max_rng = ( 0.95, 1.00 ), y_min_rng = ( 0.00, 0.05 ), y_pre_drop_dip_rng = ( 0.01, 0.05 ), \
        y_post_drop_dip_rng = ( 0.01, 0.05 ) ):

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


    def gen_data( self, n : int, x_arr ):

        data_pt_cnt = len( x_arr )
        if data_pt_cnt == 0:
            return False, False, False

        # Generate the randomized parameters for the three segments linear plot.
        drop_mid_pt_arr = np.random.uniform( self.drop_mid_pt_rng[0], self.drop_mid_pt_rng[1], size = n )
        drop_width_arr = np.random.uniform( self.drop_width_rng[0], self.drop_width_rng[1], size = n )
        y_max_arr = np.random.uniform( self.y_max_rng[0], self.y_max_rng[1], size = n )
        y_min_arr = np.random.uniform( self.y_min_rng[0], self.y_min_rng[1], size = n )
        y_pre_drop_dip_arr = np.random.uniform( self.y_pre_drop_dip_rng[0], self.y_pre_drop_dip_rng[1], size = n )
        y_post_drop_dip_arr = np.random.uniform( self.y_post_drop_dip_rng[0], self.y_post_drop_dip_rng[1], size = n )

        # The array to store the data.
        Y = np.zeros( ( n, data_pt_cnt ) )
        config_arr = [LogisticFuncConfig() for _ in range(n)]
        refPts_arr = np.zeros( ( n, 4 ) )

        # Create the logistic plot data given the specified randomization parameters.
        for z in range(n):

            # Obtain the current randomized control parameters.
            y_min_z = y_min_arr[z]
            y_max_z = y_max_arr[z]
            drop_mid_pt_z = drop_mid_pt_arr[z]
            drop_width_z = drop_width_arr[z]
            y_pre_drop_dip_z = y_pre_drop_dip_arr[z]
            y_post_drop_dip_z = y_post_drop_dip_arr[z]

            # Compute the two reference points for constructing the logistic function.
            x_a = drop_mid_pt_z - drop_width_z/2.0
            x_a = max( x_a, self.x_drop_rng_lim[0] )
            x_b = drop_mid_pt_z + drop_width_z/2.0
            x_b = min( x_b, self.x_drop_rng_lim[1] )
            y_a = y_max_z - y_pre_drop_dip_z
            y_b = y_min_z + y_post_drop_dip_z

            # Compute the logistic function parameters achieving the reference points 
            # intersect.
            config_arr[z] = fit_logistic_2_pts( x_a, y_a, x_b, y_b, y_min_z, y_max_z )

            # Obtain the plot data of the logistic function.
            y_arr_z = get_logistic_plot_data( config_arr[z], x_arr )

            # Save the plot data.
            Y[z,:] = y_arr_z[:]
            # Save the current instance of reference points used.
            refPts_arr[z][0] = x_a
            refPts_arr[z][1] = y_a
            refPts_arr[z][2] = x_b
            refPts_arr[z][3] = y_b


        return Y, config_arr, refPts_arr



class randDGen_LPL:
    '''
    A class that holds the range of possible control variables for the specific
    plot function LPL which consists of the continuous grouping of three function segments:
        [1. Linear function]
        [2. Polynomial function (Decreasing)]
        [3. Linear function]

    The class also holds a function that generate this function's plot data in
    a randomized fashion according to the defined range of possible control 
    variables.

    Attributes
    ----------
    x_ref : ( float, float )
        The start and end of the full function description over the x-axis. These
        delimiters do not vary randomly.
    x1_rng : ( float, float )
        The random range of the x position where the first linear segment transitions
        into the polynomial segment.
    x2_rng : ( float, float )
        The random range of the x position where the polynomial segment transitions
        into the second linear segment.
    y_rngs : 4 X 2 np.array
        The array holding the random range of the y position of all four points 
        (start, linear-to-poly, poly-to-linear, end).
    z_rng : ( float, float )
        The random range of the degree of the polynomial.
    u_start_rng : ( float, float )
        The random range of the portion (0.0 to 1.0) of the polynomial being forced to be 
        flat before the descent into the last linear segment.
    '''

    def __init__( self, x_ref = (0,1), x1_rng=(0.01,0.50), x2_rng=(0.30, 0.80), \
        y_rngs=np.array([[0.99, 1.00],[0.95, 0.99],[0.20, 0.06],[0.01, 0.05]]), \
        z_rng=(1.5, 10), u_start_rng = (0.05,0.7) ):

        self.x_ref = x_ref
        self.x1_rng = x1_rng
        self.x2_rng = x2_rng
        self.y_rngs = y_rngs
        self.z_rng = z_rng
        self.u_start_rng = u_start_rng

    def gen_data( self, n : int, x_arr ):

        data_pt_cnt = len( x_arr )
        if data_pt_cnt == 0:
            return False, False, False
        
        # Generate the randomized parameters for the lin-poly-lin plot.
        x1_arr = np.random.uniform( self.x1_rng[0], self.x1_rng[1], size = n )
        x2_arr = np.random.uniform( self.x2_rng[0], self.x2_rng[1], size = n )
        y0_arr = np.random.uniform( self.y_rngs[0][0], self.y_rngs[0][1], size = n )
        y1_arr = np.random.uniform( self.y_rngs[1][0], self.y_rngs[1][1], size = n )
        y2_arr = np.random.uniform( self.y_rngs[2][0], self.y_rngs[2][1], size = n )
        y3_arr = np.random.uniform( self.y_rngs[3][0], self.y_rngs[3][1], size = n )
        z_arr = np.random.uniform( self.z_rng[0], self.z_rng[1], size = n )
        u_start_arr = np.random.uniform( self.u_start_rng[0], self.u_start_rng[1], size = n )

        # Rearrange x2 points ending up below corresponding x1 points.
        a = self.x2_rng[1] - self.x2_rng[0]
        for z in range(n):
            if x1_arr[z] > x2_arr[z]:
                b = self.x2_rng[1] - x1_arr[z]
                c = x2_arr[z] - self.x2_rng[0]
                d = c*b/a
                x2_arr[z] = x1_arr[z] + d

        # The array to store the data.
        Y = np.zeros( ( n, data_pt_cnt ) )
        # The array to store the polynomial configurations
        polyCFig_arr = [PolyDropFuncConfig() for _ in range(n)]

        fourPts = np.zeros((4, 2))
        fourPts[0][0] = self.x_ref[0]
        fourPts[3][0] = self.x_ref[1]

        # Create the linear drop plot data given the specified randomization parameters.
        for i in range(n):

            # Segment connection points coordinate update.
            fourPts[1][0] = x1_arr[i]
            fourPts[2][0] = x2_arr[i]
            fourPts[0][1] = y0_arr[i]
            fourPts[1][1] = y1_arr[i]
            fourPts[2][1] = y2_arr[i]
            fourPts[3][1] = y3_arr[i]

            # Polynomial drop segment settings update.
            polyCFig_arr[i].x0 = x1_arr[i]
            polyCFig_arr[i].y0 = y1_arr[i]
            polyCFig_arr[i].x1 = x2_arr[i]
            polyCFig_arr[i].y1 = y2_arr[i]
            polyCFig_arr[i].z = z_arr[i]
            polyCFig_arr[i].u_start = u_start_arr[i]

            y_arr = gen_linPolyLin_plotData( fourPts, polyCFig_arr[i], x_arr )

            Y[i,:] = y_arr[:]

        return Y, polyCFig_arr


# ======================================================================= <<<<<

