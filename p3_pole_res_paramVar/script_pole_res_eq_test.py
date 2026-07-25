



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


from func_depo import PoleResSyst_SISO



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

do_test = True

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

