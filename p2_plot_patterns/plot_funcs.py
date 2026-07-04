



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




# ======================================================================= >>>>>
#       Linear Function Plot Tools
# ======================================================================= >>>>>

def line_segment(x_start : int, y_start : int, x_end : int, y_end : int, num_points : int = 100):
    '''
    Simple function to provide the data of a line function between two
    specified points.
    '''

    x = np.linspace(x_start, x_end, num_points)
    # y = m x + b, with m and b from the two points
    m = (y_end - y_start) / (x_end - x_start)
    b = y_start - m * x_start
    y = m * x + b
    return x, y



class LinFuncConfig:

    m = 0
    b = 0

    def __init__(self, x1 = 0, y1 = 0, x2 = 1, y2 = 1):
        self.m = ( y2 - y1 )/( x2 - x1 )
        self.b = y1 - self.m * x1

    def calibrate( self, x1 = 0, y1 = 0, x2 = 1, y2 = 1 ):
        self.m = ( y2 - y1 )/( x2 - x1 )
        self.b = y1 - self.m * x1

def get_lin_plot_data( config : LinFuncConfig, x_arr ):

    y_arr = config.m * x_arr + config.b

    return y_arr

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Logistic Function Plot Tools
# ======================================================================= >>>>>

class LogisticFuncConfig:
    '''
    Instead of low to high, this configuration goes from high to low.
        
    y = y_min + (y_max - y_min) / (1.0 + np.exp(k * (x - x0)))
    '''
    y_min = 0   # Lower limit y value.
    y_max = 1   # Upper limit y value.
    k = 1       # Logistic growth rate.
    x0 = 0      # Sigmoid's mid point.

    def __init__( self, y_min = 0, y_max = 1, k = 1, x0 = 0 ):
        self.y_min = y_min
        self.y_max = y_max
        self.k = k
        self.x0 = x0


def fit_logistic_2_pts(x_a, y_a, x_b, y_b, y_min, y_max):
    '''
    Function determines the k (logistic grownth rate) and x0 (sigmoid's mid point)
    from the given parameters

    Args:
        x_a: starting point x coordinate that the function must cross.
        y_a: starting point y coordinate that the function must cross.
        x_b: ending point x coordinate that the function must cross.
        y_b: ending point y coordinate that the function must cross.
        y_min: The lower y limit of the function (y_a and y_b must be higher than this).
        y_max: The upper y limit of the function (y_a and y_b must be lower than this).
    '''

    if y_max <= y_min:
        raise ValueError("y_max must be strictly larger than y_min")

    # Normalize y values to (0,1) range between y_min and y_max
    A = (y_a - y_min) / (y_max - y_min)
    B = (y_b - y_min) / (y_max - y_min)

    if not (0 < A < 1 and 0 < B < 1):
        raise ValueError("Points must lie strictly between y_min and y_max")

    Ea = 1.0 / A - 1.0  # = exp(k * (x_a - x0))
    Eb = 1.0 / B - 1.0  # = exp(k * (x_b - x0))

    k  = (np.log(Eb) - np.log(Ea)) / (x_b - x_a)
    x0 = x_a - np.log(Ea) / k

    return LogisticFuncConfig( y_min, y_max, k, x0 )


def get_logistic_plot_data( cfig : LogisticFuncConfig, x_arr ):

    y_arr = cfig.y_min + ( cfig.y_max - cfig.y_min ) / (1.0 + np.exp( cfig.k * ( x_arr - cfig.x0 )))

    return y_arr

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Exponential Decay Function Plot Tools
# ======================================================================= >>>>>

class PolyDropFuncConfig:
    '''
    Configuration for a polynomial function intended to be mapped over a restricted
    x range [x0,x1] and y range [y0,y1] 
    The curve starts decreasing slowly (smoothly) and ends up decreasing rapidly 
    near the end of the specified range.
    The curve must traverse points (x0,y0) and (x1,y1).

    Args:
        x0: The starting point x. Expected to be < x1
        y0: The starting point y. Expected to be > y1
        x1: The ending point x. Expected to be > x0
        y1: The ending point y. Expected to be < y0
        z: The exponential degree. Expected to be >= 2.
            Controls how flat is the beginning portion and how steep is the ending portion.
        u_start: fraction of the segment that is almost flat before dropping
              [0 -> pure 1 - u^z]
              [0.3 -> ~30% flat-ish, then drop]
    '''

    x0 = 0.0
    y0 = 1.0
    x1 = 1.0
    y1 = 0.0
    z = 2.0
    u_start = 0

    def __init__( self, x0 = 0.0, y0 = 1.0, x1 = 1.0, y1 = 0.0, z = 2.0, u_start = 0 ):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.z = z
        self.u_start = u_start
    

def get_poly_drop_plot_data( cfig : PolyDropFuncConfig, x ):
    """
    Decreasing curve from (x0, y0) to (x1, y1) shaped like 1 - u^z,
    but with control over where it starts to significantly decrease.

    The configurations in the PolyDropFuncConfig arguments are as follow:

    Args:
        x0: The starting point x. Expected to be < x1
        y0: The starting point y. Expected to be > y1
        x1: The ending point x. Expected to be > x0
        y1: The ending point y. Expected to be < y0
        z: The exponential degree. Expected to be >= 2.
            Controls how flat is the beginning portion and how steep is the ending portion.
        u_start: fraction of the segment that is almost flat before dropping
              [0 -> pure 1 - u^z]
              [0.3 -> ~30% flat-ish, then drop]
    """

    x = np.asarray(x)
    # normalize x to u in [0, 1]
    u = (x - cfig.x0) / (cfig.x1 - cfig.x0)
    
    # u = np.clip(u, 0.0, 1.0)

    # warp: keep [0, u_start] almost flat, map [u_start, 1] -> [0, 1]
    v = np.maximum(0.0, (u - cfig.u_start) / (1.0 - cfig.u_start))

    # shape function: starts near 1, then drops: 1 - v^z
    g = 1.0 - v**cfig.z

    # map g from [1 -> 0] to [y0 -> y1]
    return cfig.y1 + (cfig.y0 - cfig.y1) * g

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Special Plot Sequence Generators
# ======================================================================= >>>>>

class Lin3SegmConfig:
    '''
    Configuration for a simple three segments linear line plot.
    '''

    x1 = 0.0
    x2 = 30.0
    x3 = 70.0
    x4 = 100.0

    y1 = 10.0
    y2 = 9.8
    y3 = 1.2
    y4 = 1

    data_pt_cnt = 100

    def to_str(self):
        ret_str = f"p1=({self.x1},{self.y1}), p2=({self.x2},{self.y2})"
        ret_str += f", p3=({self.x3},{self.y3}), p4=({self.x4},{self.y4})"
        ret_str += f", data_pt_cnt({self.data_pt_cnt})"
        return ret_str

def gen_Lin3SegmPlotData( config : Lin3SegmConfig ):

    x_arr = np.linspace( config.x1, config.x4, config.data_pt_cnt )

    # Segment 1 configuration.
    l1_config = LinFuncConfig( config.x1, config.y1, config.x2, config.y2 )
    # Obtain the index of the value in x_arr immediately below and after x2.
    pre_x2_idx = np.searchsorted( x_arr, config.x2, side='left' )
    post_x2_idx = pre_x2_idx + 1
    # In case the index fall squarely on x2, decrement both.
    if x_arr[pre_x2_idx] >= config.x2:
        pre_x2_idx -= 1
        post_x2_idx -= 1

    # Segment 1 data gen.
    l1_x_arr = x_arr[ 0 : post_x2_idx ]
    l1_y_arr = get_lin_plot_data( l1_config, l1_x_arr )

    # Segment 2 configuration.
    l2_config = LinFuncConfig( config.x2, config.y2, config.x3, config.y3 )
    # Obtain the index of the value in x_arr immediately below x3.
    pre_x3_idx = np.searchsorted( x_arr, config.x3, side='left' )
    post_x3_idx = pre_x3_idx + 1
    # In case the index fall squarely on x3, decrement both.
    if x_arr[pre_x3_idx] >= config.x3:
        pre_x3_idx -= 1
        post_x3_idx -= 1
    

    # Segment 2 data gen.
    l2_x_arr = x_arr[ post_x2_idx : post_x3_idx ]
    l2_y_arr = get_lin_plot_data( l2_config, l2_x_arr )

    # Segment 3 configuration.
    l3_config = LinFuncConfig( config.x3, config.y3, config.x4, config.y4 )
    # Segment 3 data gen.
    l3_x_arr = x_arr[ post_x3_idx : ]
    l3_y_arr = get_lin_plot_data( l3_config, l3_x_arr )

    # Complete the y-axis data array.
    y_arr = np.concatenate( ( l1_y_arr, l2_y_arr, l3_y_arr ) )


    return x_arr, y_arr


def gen_linPolyLin_plotData( fourPts, poly_cfig : PolyDropFuncConfig, data_pt_cnt = 101 ):
    '''
    Generate the data of a plot consisting of a linear, semi-polynomial, and linear
    segments.

    Note that the polynomial config object "poly_cfig" will have its (x0,y0) and (x1,y1)
    being overitten by corresponding points in "fourPts"
    '''

    # Update the polynomial configuration with the present segment coordinates.
    poly_cfig.x0 = fourPts[1][0]
    poly_cfig.y0 = fourPts[1][1]
    poly_cfig.x1 = fourPts[2][0]
    poly_cfig.y1 = fourPts[2][1]

    # Define the two linear segment configurations.
    seg0_lin = LinFuncConfig( fourPts[0][0], fourPts[0][1], fourPts[1][0], fourPts[1][1] )
    seg2_lin = LinFuncConfig( fourPts[2][0], fourPts[2][1], fourPts[3][0], fourPts[3][1] )

    # Define the full x-axis point set of the plot.
    x_arr = np.linspace( fourPts[0][0], fourPts[3][0], data_pt_cnt )

    # Obtain the index of the value in x_arr immediately below x1.
    pre_x1_idx = np.searchsorted( x_arr, fourPts[1][0], side='left' )
    post_x1_idx = pre_x1_idx + 1
    # In case the index fall squarely on x1, decrement both.
    if x_arr[pre_x1_idx] >= fourPts[1][0]:
        pre_x1_idx -= 1
        post_x1_idx -= 1

    # Obtain the index of the value in x_arr immediately below x2.
    pre_x2_idx = np.searchsorted( x_arr, fourPts[2][0], side='left' )
    post_x2_idx = pre_x2_idx + 1
    # In case the index fall squarely on x2, decrement both.
    if x_arr[pre_x2_idx] >= fourPts[2][0]:
        pre_x2_idx -= 1
        post_x2_idx -= 1

    # Segment 0 data gen.
    l0_x_arr = x_arr[ 0 : post_x1_idx ]
    l0_y_arr = get_lin_plot_data( seg0_lin, l0_x_arr )

    # Segment 1 data gen.
    l1_x_arr = x_arr[ post_x1_idx : post_x2_idx ]
    l1_y_arr = get_poly_drop_plot_data( poly_cfig, l1_x_arr )

    # Segment 2 data gen.
    l2_x_arr = x_arr[ post_x2_idx : ]
    l2_y_arr = get_lin_plot_data( seg2_lin, l2_x_arr )

    # Complete the y-axis data array.
    y_arr = np.concatenate( ( l0_y_arr, l1_y_arr, l2_y_arr ) )


    return x_arr, y_arr

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Linear Function Plot Tests
# ======================================================================= >>>>>

do_test = False

if do_test:

    myConfig = Lin3SegmConfig()

    myConfig.x1 = 0;        myConfig.y1 = 0.9
    myConfig.x2 = 0.2;      myConfig.y2 = 0.85
    myConfig.x3 = 0.4;      myConfig.y3 = 0.12
    myConfig.x4 = 1;        myConfig.y4 = 0.1

    myConfig.data_pt_cnt = 41

    x_arr, y_arr = gen_Lin3SegmPlotData( myConfig )


    plt.plot( x_arr, y_arr )
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("y = x")
    plt.grid(True)
    plt.show()

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       Logistic Function Plot Tests
# ======================================================================= >>>>>

do_test = False

if do_test:

    x_a = 0.6;        y_a = 0.9
    x_b = 0.7;        y_b = 0.1
    y_min = 0;   y_max = 1

    myConfig = fit_logistic_2_pts(x_a, y_a, x_b, y_b, y_min, y_max)

    x_arr = np.linspace( 0, 1, 100 )

    y_arr = get_logistic_plot_data( myConfig, x_arr )

    plt.plot( x_arr, y_arr )
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Logistic Drop")
    plt.grid(True)
    plt.show()

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       Poly Drop Function Plot Tests
# ======================================================================= >>>>>

do_test = False

if do_test:

    cfig = PolyDropFuncConfig()

    cfig.x0 = 0
    cfig.y0 = 1
    cfig.x1 = 1
    cfig.y1 = 0
    cfig.z = 10.0
    cfig.u_start = 0.1

    x_arr = np.linspace( 0, 1, 100 )

    y_arr = get_poly_drop_plot_data( cfig, x_arr )

    plt.plot( x_arr, y_arr )
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Semi-Polynomial Drop")
    plt.grid(True)
    plt.show()

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       gen_linPolyLin_plotData Plot Tests
# ======================================================================= >>>>>

do_test = False

if do_test:

    fourPts = np.zeros((4, 2))
    fourPts[0][0] = 0.0;  fourPts[0][1] = 1.00
    fourPts[1][0] = 0.2;  fourPts[1][1] = 0.98
    fourPts[2][0] = 0.8;  fourPts[2][1] = 0.05
    fourPts[3][0] = 1.0;  fourPts[3][1] = 0.02

    poly_cfig = PolyDropFuncConfig()
    poly_cfig.z = 4.0
    poly_cfig.u_start = 0.2

    data_pt_cnt = 101

    x_arr, y_arr = gen_linPolyLin_plotData( fourPts, poly_cfig, data_pt_cnt )

    plt.plot( x_arr, y_arr )
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Segmented Semi-Polynomial Drop")
    plt.grid(True)
    plt.show()





# ======================================================================= <<<<<
