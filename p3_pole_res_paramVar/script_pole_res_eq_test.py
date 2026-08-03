



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
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
from toolbox.dataUtils import convert_cconj_to_ReIm_format
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

# Simple random pole-residue system generation test.
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



do_test = True

# Random single parameter parametrization test.
if do_test:

    # Define current test's numerical floor.
    tol = 1e-12

    # Define the umber of system poles.
    poleRes_cnt = 8

    # Generate the reference poles-res system.
    mySyst = PoleResSyst_SISO.gen_rand_syst( poleRes_cnt )

    # Use the reference system to create a full set of randomly generated pole-res 
    # systems created based on the reference system which has its poles and residues varying 
    # over a single abstract parameter using randomly generated rational functions.
    pole_arr, res_arr = PoleResSyst_SISO.gen_rand_1param_var( mySyst )

    # Obtain the number of sample abstract parameter points.
    p_cnt = pole_arr.shape[0]

    # Define a generic normalized parameter array.
    p_arr = np.linspace( 0, 1, p_cnt )

    do_plots = False
    # Poles and residues real and imaginary part plots.
    if do_plots:

        print( "System pole/res count: ", poleRes_cnt )
        print( "System poles at p=0: " )
        print( pole_arr[0,:] )
        print( pole_arr[10,:] )
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        fig3, ax3 = plt.subplots()
        fig4, ax4 = plt.subplots()

        for z in range( poleRes_cnt ):
            pole_arr_z = pole_arr[:,z]
            res_arr_z = res_arr[:,z]
            ax1.plot( p_arr, pole_arr_z.real )
            ax2.plot( p_arr, pole_arr_z.imag )
            ax3.plot( p_arr, res_arr_z.real )
            ax4.plot( p_arr, res_arr_z.imag )
            
        # Pole real part plot.
        ax1.set_title("Pole Real Part")
        ax1.set_xlabel("p")
        ax1.set_ylabel("pole real part")
        ax1.legend( ["pole re"] )
        ax1.grid( True, 'both' )
        # Pole Imaginary part plot.
        ax2.set_title("Pole Imag Part")
        ax2.set_xlabel("p")
        ax2.set_ylabel("pole imag part")
        ax2.legend( ["pole im"] )
        ax2.grid( True, 'both' )
        # Residues real part plot.
        ax3.set_title("Residues Real Part")
        ax3.set_xlabel("p")
        ax3.set_ylabel("res real part")
        ax3.legend( ["res re"] )
        ax3.grid( True, 'both' )
        # Residues imag part plot.
        ax4.set_title("Residues Imag Part")
        ax4.set_xlabel("p")
        ax4.set_ylabel("res imag part")
        ax4.legend( ["res im"] )
        ax4.grid( True, 'both' )

        plt.show()



    # Initialize an array of SISO pole-residue systems.
    syst_arr = [ PoleResSyst_SISO() for _ in range(p_cnt) ]

    # Assign each system with their intended poles and residues sets and compute
    # and store the system's transfer function over the sampling frequency range.
    for z in range( p_cnt ):

        # Obtain the current poles and residues.
        pole_arr_z = pole_arr[z,:]
        res_arr_z = res_arr[z,:]
        # Assign the current poles and residues to their system.
        syst_arr[z].poles = pole_arr_z
        syst_arr[z].residues = res_arr_z
        


    do_plots = True
    # 2D system magnitude plot.
    if do_plots:

        # Define the frequency sampling array.
        f_cnt = 500
        f_arr = np.linspace( 0, 100, f_cnt )
        # Define the array of sampled transfer function.
        S_arr = np.zeros( (p_cnt, f_cnt), dtype=complex )
        for z in range( p_cnt ):
            # Obtain current system frequency data.
            S_arr[z,:] = syst_arr[z].freq_response( f_arr )
        
        fig1, ax1 = plt.subplots()
        for z in range( p_cnt ):
            ax1.plot( f_arr, abs( S_arr[z,:] ) )

        # Pole real part plot.
        ax1.set_title("S-man Plot")
        ax1.set_xlabel("x")
        ax1.set_ylabel("S-mag")
        ax1.grid( True, 'both' )

        plt.show()

    do_plots = False
    # 3D System magnitude and phase plots.
    if do_plots:
        P, X = np.meshgrid(f_arr, p_arr, indexing='xy')  # match S_arr shape
        print( P.shape )
        print( X.shape )

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_surface(P, X, abs( S_arr ), cmap='viridis')

        ax.set_xlabel('x')
        ax.set_ylabel('p')
        ax.set_zlabel('S')

        plt.show()


    # Define poles and residues arrays with just real and imaginary part magnitudes.
    pole_mag_arr = np.zeros( ( p_cnt, poleRes_cnt ), dtype=float )
    res_mag_arr = np.zeros( ( p_cnt, poleRes_cnt ), dtype=float )
    # Define boolean map keeping track whether a value is complex conjugate or not.
    pole_cconj_map = np.zeros( ( p_cnt, poleRes_cnt ), dtype=bool )
    res_cconj_map = np.zeros( ( p_cnt, poleRes_cnt ), dtype=bool )

    # Flag for complex conjugate case signaling and loop skipping.
    cconj_flag = False
    # Reconfigure pole and residue arrays so they are stored as real and imag parts rather than
    # complex values.
    for i in range( p_cnt ):
        
        pole_mag_i, pole_cconj_map_i = convert_cconj_to_ReIm_format( pole_arr[i,:] )
        pole_mag_arr[i,:] = pole_mag_i
        pole_cconj_map[i,:] = pole_cconj_map_i

        res_mag_i, res_cconj_map_i = convert_cconj_to_ReIm_format( res_arr[i,:] )
        res_mag_arr[i,:] = res_mag_i
        res_cconj_map[i,:] = res_cconj_map_i
            
    
    # Compute the column wise maximum magnitude.
    scale_p = np.max( np.abs( pole_mag_arr ), axis = 0 )
    scale_r = np.max( np.abs( res_mag_arr ), axis = 0 )
    # For columns having 0 max magnitude, force the scaling factor to 1
    scale_p[ scale_p == 0 ] = 1.0
    scale_r[ scale_r == 0 ] = 1.0

    # normalize (broadcast over rows).
    pole_mag_norm = pole_mag_arr / scale_p[np.newaxis, :]
    res_mag_norm = res_mag_arr / scale_r[np.newaxis, :]



    # To undo normalization later:
    # pole_arr_recovered = pole_mag_norm * scale_p[np.newaxis, :]
    # res_arr_recovered  = res_mag_norm  * scale_r[np.newaxis, :]


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



do_test = False

# Rational function generation using randomized poles as starting point.
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

