


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

class LinFuncConfig:

    m = 0
    b = 0

    def __init__(self, x1 = 0, y1 = 0, x2 = 1, y2 = 1):
        self.m = ( y2 - y1 )/( x2 - x1 )
        self.b = y1 - self.m * x1


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

def get_lin_plot_data( config : LinFuncConfig, x_arr ):

    y_arr = config.m * x_arr + config.b

    return y_arr



def gen_Lin3SegmPlotData( config : Lin3SegmConfig ):


    x_arr = np.linspace( config.x1, config.x4, config.data_pt_cnt )

    # Segment 1 configuration.
    l1_config = LinFuncConfig( config.x1, config.y1, config.x2, config.y2 )
    # Obtain the index of the value in x_arr immediately below x2.
    x2_idx = np.searchsorted( x_arr, config.x2, side='right' ) - 1
    # Segment 1 data gen.
    l1_x_arr = x_arr[ 0 : x2_idx ]
    l1_y_arr = get_lin_plot_data( l1_config, l1_x_arr )

    # Segment 2 configuration.
    l2_config = LinFuncConfig( config.x2, config.y2, config.x3, config.y3 )
    # Obtain the index of the value in x_arr immediately below x3.
    x3_idx = np.searchsorted( x_arr, config.x3, side='right' ) - 1
    # Segment 2 data gen.
    l2_x_arr = x_arr[ x2_idx : x3_idx ]
    l2_y_arr = get_lin_plot_data( l2_config, l2_x_arr )

    # Segment 3 configuration.
    l3_config = LinFuncConfig( config.x3, config.y3, config.x4, config.y4 )
    # Segment 3 data gen.
    l3_x_arr = x_arr[ x3_idx : ]
    l3_y_arr = get_lin_plot_data( l3_config, l3_x_arr )

    # Complete the y-axis data array.
    y_arr = np.concatenate( ( l1_y_arr, l2_y_arr, l3_y_arr ) )


    return x_arr, y_arr


myConfig = Lin3SegmConfig
myConfig.data_pt_cnt = 41

x_arr, y_arr = gen_Lin3SegmPlotData( myConfig )

# print( x_arr )
# print( y_arr )

plt.plot( x_arr, y_arr )
plt.xlabel("x")
plt.ylabel("y")
plt.title("y = x")
plt.grid(True)
plt.show()

