


import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import numbers
import numpy as np
import pandas as pd
import random


from scipy import signal
from toolbox.dataUtils import random_in_range
from toolbox.dataUtils import random_re_poly_roots


class PoleResSyst_SISO:
    """
    SISO LTI system in pole–residue form:
        H(s) = d + sum_i { r_i / (s - p_i) }
    """

    def __init__( self, residues=None, poles=None, direct=0.0 ):
        self.residues = np.array(residues, dtype=complex) if residues is not None else np.array([], dtype=complex)
        self.poles    = np.array(poles,    dtype=complex) if poles    is not None else np.array([], dtype=complex)
        # Make sure equal number of residues and poles.
        assert self.residues.shape == self.poles.shape
        self.direct   = complex(direct)  # constant term d

    def H(self, s):
        """
        Evaluate H(s) for scalar or array s.
        """

        s = np.asarray(s, dtype=complex)
        Hs = np.zeros_like(s, dtype=complex) + self.direct
        for r, p in zip( self.residues, self.poles ):
            Hs += r / (s - p)
        return Hs

    def freq_response(self, w):
        """
        Evaluate H(j*w) for real frequency array w.
        """
        
        w = np.asarray(w, dtype=float)
        s = 1j * w
        return self.H(s)
    

    @staticmethod
    def gen_rand_syst( n : int ):
        '''
        Generate a SISO pole-residue system with randomized poles and
        residues (S-param system).

        Randomization is not pure, as range of allowed values are specified in
        the function to give a flavor of somewhat realistic frequency response.

        Note that such a system generated in a semi-random manner may not make sense as
        a real circuit frequency response.

        Args:
            n (int): Number of pole-residue pairs.
        '''

        # Define the range of real and image parts ranges.
        res_re_rng = ( -0.1, 0.1 )
        res_im_rng = ( -1, 1 )
        poles_re_rng = ( -10, -1 )
        poles_im_rng = ( -100, 100 )
        direct_rng = ( 0, 0.1 )

        # Real pole count random selection.
        if n <= 1:
            r_cnt = n
        else:
            # Select a m that is less than n but ensures n-m is even.
            candidates = [ m for m in range(1, n) if (n - m) % 2 == 0 ]
            r_cnt = random.choice( candidates )

        # Determine the number of complex conjugate pairs given real poles count is defined now.
        cp_cj_pair_cnt = int( np.floor( ( n - r_cnt )/2 ) )

        # Initialize the system.
        mySyst = PoleResSyst_SISO()

        # System's direct term definition.
        mySyst.direct = random_in_range( direct_rng[0], direct_rng[1], 1 )

        # System's real poles and residuals random selection.
        poles_r = random_in_range( poles_re_rng[0], poles_re_rng[1], r_cnt )
        res_r = random_in_range( res_re_rng[0], res_re_rng[1], r_cnt )

        # Define odd and even interleaving index arrays.
        even_idx = np.zeros( 2*cp_cj_pair_cnt, dtype=bool )
        even_idx[::2] = True    # every other element, starting at 0
        odd_idx = ~even_idx

        # System's complex poles and residuals random selection with explicit complex 
        # conjugacy.
        poles_cp_tmp = random_in_range( poles_re_rng[0], poles_re_rng[1], cp_cj_pair_cnt ) + \
            1j * random_in_range( poles_im_rng[0], poles_im_rng[1], cp_cj_pair_cnt )
        res_cp_tmp = random_in_range( res_re_rng[0], res_re_rng[1], cp_cj_pair_cnt ) + \
            1j * random_in_range( res_im_rng[0], res_im_rng[1], cp_cj_pair_cnt )
        poles_cp_cj = np.conjugate( poles_cp_tmp )
        res_cp_cj = np.conjugate( res_cp_tmp )
        # Assemble the complex conjugate poles in pairs.
        poles_cp = np.zeros( 2*cp_cj_pair_cnt, dtype=complex )
        poles_cp[even_idx] = poles_cp_tmp
        poles_cp[odd_idx] = poles_cp_cj
        # Assemble the complex conjugate residues in pairs.
        res_cp = np.zeros( 2*cp_cj_pair_cnt, dtype=complex )
        res_cp[even_idx] = res_cp_tmp
        res_cp[odd_idx] = res_cp_cj

        # Insert the complete sets of poles and residues into the system object.
        mySyst.residues = np.concatenate( ( res_r, res_cp ) )
        mySyst.poles = np.concatenate( ( poles_r, poles_cp ) )


        return mySyst
    
    @staticmethod
    def gen_rand_1param_var( tarSyst ):
        '''
        Create a series of pole-residue systems that are reflective of parametric
        variation with respect to 1 parameter generated in a semi-random fashion.
        '''

        assert isinstance( tarSyst, PoleResSyst_SISO ), f"tarSyst must be PoleResSyst_SISO, got {type(tarSyst)}"
        # assert isinstance( p_rng, ( numbers.Number, numbers.Number ) ), f"p_rng must be (numbers.Number,numbers.Number), got {type(p_rng)}"

        '''
        Generate core randomized rational function that serves as the basis of parametric
        variation profile.
        '''

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


        func_raw = lambda x: num_poly(x)/denom_poly(x)

        '''
        Adjustment to the generated rational function.
        '''

        # The number of sample points.
        samp_cnt = 200
        # The effective range of the random rational function.
        p_rng = ( 0, 2 )
        # The sampling set.
        p_arr = np.linspace( p_rng[0], p_rng[1], samp_cnt )
        # The sample data.
        y_raw_arr = func_raw( p_arr )

        # Determine the function range over the effective range.
        y_raw_rng = ( min( y_raw_arr ), max( y_raw_arr ) )
        # The amplitude of the function over the effective range.
        y_raw_amp = y_raw_rng[1] - y_raw_rng[0]

        # Define the adjusted amplitude.
        y_adj_amp = 0.5
        # Define the scaling factor for the rational function to reach the intended
        # amplitude over the effective range.
        y_scale_fact = y_adj_amp / y_raw_amp
        
        func_adj = lambda x: ( func_raw(x) - y_raw_rng[0] ) * y_scale_fact

        y_adj_arr = func_adj( p_arr )

        plt.plot( p_arr, y_raw_arr )
        plt.plot( p_arr, y_adj_arr )
        plt.xlabel("p")
        plt.ylabel("y")
        plt.title("Rat. Func.")
        plt.grid(True)
        plt.show()

        return 0