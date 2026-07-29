


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
from toolbox.dataUtils import random_fitted_re_rat_func


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

        The input poles-res system is assumed to be strictly real, which means its
        residues and poles all come either in real values or complex conjugate pairs.
        '''

        

        assert isinstance( tarSyst, PoleResSyst_SISO ), f"tarSyst must be PoleResSyst_SISO, got {type(tarSyst)}"
        # assert isinstance( p_rng, ( numbers.Number, numbers.Number ) ), f"p_rng must be (numbers.Number,numbers.Number), got {type(p_rng)}"

        tol = 1e-12

        syst_pole_cnt = len( tarSyst.poles )
        tarSyst.residues
        tarSyst.direct

        '''
        Generate core randomized rational function that serves as the basis of parametric
        variation profile.
        '''

        num_cnt = random.randint( 8, 10 )       # Number of numerator coefficients.
        num_rng = ( -1, 1 )                     # Numerator coefficient value range.
        # Randomly generate the set of numerical polynomial coefficients.
        num_coeff_arr =   random_in_range( num_rng[0], num_rng[1], num_cnt )

        # Set the number of poles.
        denom_cnt = num_cnt
        if denom_cnt % 2 != 0:
            denom_cnt += 1
        
        # Define numerical ranges of poles.
        poles_re_rng = ( -1, 1 )
        poles_im_rng = ( -1, 1 )
    
        # The effective range of the random rational function.
        p_rng = ( 0, 1 )

        # Define variation factor (percentage of allowed change in decimal).
        var_fact = 0.1
        # Define the number of parameter points to sample.
        p_cnt = 200
        # Define the parameter sampling set.
        p_arr = np.linspace( p_rng[0], p_rng[1], p_cnt )

        # Define the array housing all the poles.
        pole_arr = np.zeros( ( p_cnt, syst_pole_cnt ), dtype=np.complex128 )
        

        # print( "System pole/res count: ", syst_pole_cnt )
        # print( "System base poles: \n", tarSyst.poles )
        # fig1, ax1 = plt.subplots()
        # fig2, ax2 = plt.subplots()

        cplx_conj_iter = False
        for z in range( syst_pole_cnt ):

            # If complex conjugate case detected previously, skip current iteration.
            if cplx_conj_iter:
                cplx_conj_iter = False
                continue
            
            # Obtain the current pole.
            base_pole_z = tarSyst.poles[z]

            # Verify if current pole imaginary part is present, in which case we have 
            # detected a complex conjugate pair.
            cplx_conj_iter = abs( base_pole_z.imag ) > tol

            # Obtain the allowed change in poles real part.
            y_pole_re_adj_amp_z = abs( base_pole_z.real )*var_fact
            # Obtain variation function for the real parts of the pole.
            pole_re_mod_func_z, _, _ = random_fitted_re_rat_func( num_cnt, denom_cnt, num_rng, \
                poles_re_rng, poles_im_rng, p_rng, y_pole_re_adj_amp_z )

            if cplx_conj_iter:

                # Obtain the allowed change in poles imaginary.
                y_pole_im_adj_amp_z = abs( base_pole_z.imag )*var_fact
                # Obtain variation function for the imaginary parts of the pole.
                pole_im_mod_func_z, _, _ = random_fitted_re_rat_func( num_cnt, denom_cnt, num_rng, \
                    poles_re_rng, poles_im_rng, p_rng, y_pole_im_adj_amp_z )

                # Add the current modified pole set.
                pole_arr_z = base_pole_z + ( pole_re_mod_func_z( p_arr ) + 1j*pole_im_mod_func_z( p_arr ) )
                pole_arr[:,z] = pole_arr_z[:]
                # Add the complex conjugate modified pole set.
                pole_arr_z = base_pole_z + ( pole_re_mod_func_z( p_arr ) - 1j*pole_im_mod_func_z( p_arr ) )
                pole_arr[:,z+1] = pole_arr_z[:]

            else:

                # Add the current modified pole set.
                pole_arr_z = base_pole_z + pole_re_mod_func_z( p_arr )
                pole_arr[:,z] = pole_arr_z[:]

            # ax1.plot( p_arr, pole_arr_z.real )
            # ax2.plot( p_arr, pole_arr_z.imag )
            
        # ax1.set_title("Pole Real Part")
        # ax1.set_xlabel("p")
        # ax1.set_ylabel("pole real part")
        # ax1.legend( ["pole re"] )
        # ax1.grid( True, 'both' )
        # ax2.set_title("Pole Imag Part")
        # ax2.set_xlabel("p")
        # ax2.set_ylabel("pole imag part")
        # ax2.legend( ["pole im"] )
        # ax2.grid( True, 'both' )
        # plt.show()
    

        # Define the array housing all the residues.
        res_arr = np.zeros( ( p_cnt, syst_pole_cnt ), dtype=np.complex128 )

        # print( "System pole/res count: ", syst_pole_cnt )
        # print( "System base residues: \n", tarSyst.residues )
        # fig1, ax1 = plt.subplots()
        # fig2, ax2 = plt.subplots()

        cplx_conj_iter = False
        for z in range( syst_pole_cnt ):

            # If complex conjugate case detected previously, skip current iteration.
            if cplx_conj_iter:
                cplx_conj_iter = False
                continue

            # Obtain the current residues.
            base_res_z = tarSyst.residues[z]

            # Verify if current residue imaginary part is present, in which case we have 
            # detected a complex conjugate pair.
            cplx_conj_iter = abs( base_res_z.imag ) > tol

            # Obtain the allowed change in residues real part.
            y_res_re_adj_amp_z = abs( base_res_z.real )*var_fact
            # Obtain variation function for the real parts of the res.
            res_re_mod_func_z, _, _ = random_fitted_re_rat_func( num_cnt, denom_cnt, num_rng, \
                poles_re_rng, poles_im_rng, p_rng, y_res_re_adj_amp_z )            

            if cplx_conj_iter:

                # Obtain the allowed change in res imaginary.
                y_res_im_adj_amp_z = abs( base_res_z.imag )*var_fact
                # Obtain variation function for the imaginary parts of the res.
                res_im_mod_func_z, _, _ = random_fitted_re_rat_func( num_cnt, denom_cnt, num_rng, \
                    poles_re_rng, poles_im_rng, p_rng, y_res_im_adj_amp_z )

                # Add the current modified res set.
                res_arr_z = base_res_z + ( res_re_mod_func_z( p_arr ) + 1j*res_im_mod_func_z( p_arr ) )
                res_arr[:,z] = res_arr_z[:]
                # Add the complex conjugate modified res set.
                res_arr_z = base_res_z + ( res_re_mod_func_z( p_arr ) - 1j*res_im_mod_func_z( p_arr ) )
                res_arr[:,z+1] = res_arr_z[:]

            else:

                # Add the current modified res set.
                res_arr_z = base_res_z + res_re_mod_func_z( p_arr )
                res_arr[:,z] = res_arr_z[:]

            # ax1.plot( p_arr, res_arr_z.real )
            # ax2.plot( p_arr, res_arr_z.imag )

        # ax1.set_title("Res Real Part")
        # ax1.set_xlabel("p")
        # ax1.set_ylabel("res real part")
        # ax1.legend( ["res re"] )
        # ax1.grid( True, 'both' )
        # ax2.set_title("Res Imag Part")
        # ax2.set_xlabel("p")
        # ax2.set_ylabel("res imag part")
        # ax2.legend( ["res im"] )
        # ax2.grid( True, 'both' )
        # plt.show()

        return pole_arr, res_arr