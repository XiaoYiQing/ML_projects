



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
    print( roots )

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



do_test = False

if do_test:

    num_cnt = random.randint( 1, 10 )       # Number of numerator coefficients.
    num_rng = ( -1, 1 )                     # Numerator coefficient value range.

    # Randomly generate the set of numerical polynomial coefficients.
    num_coeff_arr =   random_in_range( num_rng[0], num_rng[1], num_cnt )

    

    # Set the number of poles.
    denom_cnt = num_cnt + 1

    # Real pole count random selection.
    if denom_cnt <= 1:
        r_cnt = denom_cnt
    else:
        # Select a m that is less than n but ensures n-m is even.
        candidates = [ m for m in range(1, denom_cnt) if (denom_cnt - m) % 2 == 0 ]
        r_cnt = random.choice( candidates )

    # Determine the number of complex conjugate pairs given real poles count is defined now.
    cp_cj_pair_cnt = int( np.floor( ( denom_cnt - r_cnt )/2 ) )

    # Range of poles.
    poles_re_rng = ( -5, 5 )
    poles_im_rng = ( -10, 10 )

    # Define odd and even interleaving index arrays.
    even_idx = np.zeros( 2*cp_cj_pair_cnt, dtype=bool )
    even_idx[::2] = True    # every other element, starting at 0
    odd_idx = ~even_idx
    # System's complex poles and residuals random selection with explicit complex 
    # conjugacy.
    poles_cp_tmp = random_in_range( poles_re_rng[0], poles_re_rng[1], cp_cj_pair_cnt ) + \
        1j * random_in_range( poles_im_rng[0], poles_im_rng[1], cp_cj_pair_cnt )
    poles_cp_cj = np.conjugate( poles_cp_tmp )
    # Assemble the complex conjugate poles in pairs.
    poles_cp = np.zeros( 2*cp_cj_pair_cnt, dtype=complex )
    poles_cp[even_idx] = poles_cp_tmp
    poles_cp[odd_idx] = poles_cp_cj
    


# ======================================================================= <<<<<

