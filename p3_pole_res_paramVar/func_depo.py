


import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )



import numpy as np
import pandas as pd
import random
from toolbox.dataUtils import random_in_range


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
        The default range for poles is [ -1, -0.05 )
        The default range for residues is [ -1, 1 )
        The default range for the direct term is [ 0, 1 )

        Note that such a system generated in a semi-random manner may not make sense as
        a real circuit frequency response.
        '''

        # Define the range of real and image parts ranges.
        res_re_rng = ( -1, 1 )
        res_im_rng = ( -1, 1 )
        poles_re_rng = ( -1, 0 )
        poles_im_rng = ( -1, 1 )
        direct_rng = ( 0, 1 )

        if n <= 1:
            r_cnt = n
        else:
            # Select a m that is less than n but ensures n-m is even.
            candidates = [ m for m in range(1, n) if (n - m) % 2 == 0 ]
            r_cnt = random.choice( candidates )

        # Determine the number of complex conjugate pairs.
        cp_cj_pair_cnt = ( n - r_cnt )/2

        

        mySyst = PoleResSyst_SISO()
        mySyst.direct = random_in_range( direct_rng[0], direct_rng[1], 1 )
        poles_r = random_in_range( poles_re_rng[0], poles_re_rng[1], r_cnt )
        poles_cp = random_in_range( poles_re_rng[0], poles_re_rng[1], cp_cj_pair_cnt ) + \
            1j * random_in_range( poles_im_rng[0], poles_im_rng[1], cp_cj_pair_cnt )
        poles_cp_cj = np.conjugate( poles_cp )
        

        mySyst.residues = random_in_range( -1, 1, n ) + 1j*random_in_range( -1, 1, n )

        return 0