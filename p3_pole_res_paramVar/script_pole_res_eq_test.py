



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
import random

from func_depo import PoleResSyst_SISO
from toolbox.dataUtils import random_in_range
from toolbox.dataUtils import random_re_poly_roots


# ======================================================================= >>>>>
#       Simple Case
# ======================================================================= >>>>>

do_test = False

if do_test:

    # H(s) = d + r1/(s - p1) + r2/(s - p2)
    residues = [ 1+0j, 0.5-0.2j ]
    poles    = [-1+2j, -3-1j]
    d        = 0.1

    sys = PoleResSyst_SISO( residues=residues, poles=poles, direct=d )

    w = np.linspace(0, 10, 500)
    Hjw = sys.freq_response(w)


    plt.plot( w, abs( Hjw ) )
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("y = x")
    plt.grid(True)
    plt.show()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       PoleResSyst_SISO Test
# ======================================================================= >>>>>

do_test = False

if do_test:

    mySyst = PoleResSyst_SISO.gen_rand_syst( 14 )

    x_arr = np.linspace( -100, 100, 400 )
    S_arr = mySyst.freq_response( x_arr )


    plt.plot( x_arr, abs( S_arr ) )
    plt.xlabel("x")
    plt.ylabel("S_mag")
    plt.title("S-param Magnitude")
    plt.grid(True)
    plt.show()

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       Polynomial Test
# ======================================================================= >>>>>

do_test = False

if do_test:

    # Numerator: 2x + 1
    # num_coeff_arr = [2, 1]

    num_cnt = random.randint( 1, 10 )       # Number of numerator coefficients.
    denom_cnt = num_cnt + 1                 # Number of denominator coefficients.
    num_rng = ( -1, 1 )                     # Numerator coefficient value range.
    denom_rng = ( -5, 5 )                   # Denominator coefficient value range.

    # Randomly generate the set of numerical polynomial coefficients.
    num_coeff_arr =   random_in_range( num_rng[0], num_rng[1], num_cnt )
    # Randomly generate the set of denominator polynomial coefficients.
    denom_coeff_arr = random_in_range( denom_rng[0], denom_rng[1], denom_cnt )

    num_poly = np.poly1d( num_coeff_arr )
    den_poly = np.poly1d( denom_coeff_arr )

    # Obtain the roots of the denominator.
    roots = den_poly.r

    def rat_func(x):
        return num_poly(x)/den_poly(x)


    x_arr = np.linspace( 0, 10, 100 )
    y_arr = rat_func( x_arr )

    plt.plot( x_arr, y_arr )
    plt.xlabel("x")
    plt.ylabel("S_mag")
    plt.title("S-param Magnitude")
    plt.grid(True)
    plt.show()



do_test = True

if do_test:

    num_cnt = random.randint( 6, 10 )       # Number of numerator coefficients.
    num_rng = ( -1, 1 )                     # Numerator coefficient value range.

    # Randomly generate the set of numerical polynomial coefficients.
    num_coeff_arr =   random_in_range( num_rng[0], num_rng[1], num_cnt )

    # Set the number of poles.
    denom_cnt = num_cnt

    # Define numerical ranges of poles.
    poles_re_rng = ( -1, 1 )
    poles_im_rng = ( -1, 1 )

    # Generate real polynomial roots (poles) set.
    denom_roots = random_re_poly_roots( denom_cnt, poles_re_rng, poles_im_rng, False )

    num_poly = np.poly1d( num_coeff_arr )
    denom_coeff_arr = np.poly( denom_roots )
    denom_poly = np.poly1d( denom_coeff_arr )

    print( denom_roots )
    
    def rat_func(x):
        return num_poly(x)/denom_poly(x)

    x_arr = np.linspace( 0, 2, 200 )
    y_arr = rat_func( x_arr )
    
    plt.plot( x_arr, y_arr )
    plt.xlabel("x")
    plt.ylabel("S_mag")
    plt.title("S-param Magnitude")
    plt.grid(True)
    plt.show()

# ======================================================================= <<<<<

