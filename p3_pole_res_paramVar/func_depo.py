


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
    def gen_rand_1param_var( tarSyst, var_fact = 0.2, p_cnt=500 ):
        '''
        Create a series of pole-residue systems that are reflective of parametric
        variation with respect to 1 parameter generated in a semi-random fashion.

        The input poles-res system is assumed to be strictly real, which means its
        residues and poles all come either in real values or complex conjugate pairs.

        Args:
            tarSyst: Target SISO pole-res system.
            p_cnt: The number of parameter points (linear distribution).
            var_fact: variation factor (percentage of allowed change in decimal).
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

        # Define the parameter sampling set.
        p_arr = np.linspace( p_rng[0], p_rng[1], p_cnt )

        # Define the array housing all the poles.
        pole_arr = np.zeros( ( p_cnt, syst_pole_cnt ), dtype=np.complex128 )
    

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

                base_pole_z = tarSyst.poles[z+1]
                # Add the complex conjugate modified pole set.
                pole_arr_z = base_pole_z + ( pole_re_mod_func_z( p_arr ) - 1j*pole_im_mod_func_z( p_arr ) )
                pole_arr[:,z+1] = pole_arr_z[:]

            else:

                # Add the current modified pole set.
                pole_arr_z = base_pole_z + pole_re_mod_func_z( p_arr )
                pole_arr[:,z] = pole_arr_z[:]
    

        # Define the array housing all the residues.
        res_arr = np.zeros( ( p_cnt, syst_pole_cnt ), dtype=np.complex128 )


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

                base_res_z = tarSyst.residues[z+1]
                # Add the complex conjugate modified res set.
                res_arr_z = base_res_z + ( res_re_mod_func_z( p_arr ) - 1j*res_im_mod_func_z( p_arr ) )
                res_arr[:,z+1] = res_arr_z[:]

            else:

                # Add the current modified res set.
                res_arr_z = base_res_z + res_re_mod_func_z( p_arr )
                res_arr[:,z] = res_arr_z[:]


        return pole_arr, res_arr





def random_re_poly_roots( rt_cnt = 10, rt_re_rng = ( -1, 1 ), rt_im_rng = ( -1, 1 ), \
  re_r = False, tol = 1e-9 ):
  '''
  Generate a set of roots for a polynomial that is strictly real.
  The roots may be either real or complex conjugate pairs.

  Args:
    rt_cnt (int): The number of roots to be created.
    rt_re_rng ( (float, float) ): The range of root real parts allowed.
    rt_im_rng ( (float, float) ): The range of root imaginary parts allowed.
    re_r (bool): Flag indicating whether real roots are allowed. Number of real roots
      is randomly selected. If false, rt_cnt MUST be even.
    tol: magnitude threshold of how small the imaginary part of complex roots can be.
  '''

  if ( not re_r ) and ( rt_cnt % 2 != 0 ):
      raise ValueError(f"No real root flag is raised, but number of roots requested is not even.")

  # TODO: If tol is close to one limit, it might take too many rerolls to get valid entry.
  if tol > abs( rt_im_rng[0] ) or tol > abs( rt_im_rng[1] ):
      raise ValueError( f"Root imaginary part magnitude threadhold higher than smallest imaginary value limit." )

  # Real root count random selection.
  if not re_r:
      re_rt_cnt = 0
  elif rt_cnt <= 1:
      re_rt_cnt = rt_cnt
  else:
      # Select a m that is less than n but ensures n-m is even.
      candidates = [ m for m in range(1, rt_cnt) if (rt_cnt - m) % 2 == 0 ]
      re_rt_cnt = random.choice( candidates )

  # Determine the number of complex conjugate pairs given real roots count is defined now.
  cp_cj_pair_cnt = int( np.floor( ( rt_cnt - re_rt_cnt )/2 ) )

  # System's complex roots and residuals random selection with explicit complex 
  # conjugacy.
  roots_cp_tmp = random_in_range( rt_re_rng[0], rt_re_rng[1], cp_cj_pair_cnt ) + \
      1j * random_in_range( rt_im_rng[0], rt_im_rng[1], cp_cj_pair_cnt )
  
  # Reroll the root if it has 0 imaginary part.
  for z in range( cp_cj_pair_cnt ):
    while abs( roots_cp_tmp[z].imag ) < tol:
      roots_cp_tmp[z] = complex( roots_cp_tmp[z].real, random_in_range( rt_im_rng[0], rt_im_rng[1], 1 )[0] )
  
  roots_cp_cj = np.conjugate( roots_cp_tmp )

  # Define odd and even interleaving index arrays.
  even_idx = np.zeros( 2*cp_cj_pair_cnt, dtype=bool )
  even_idx[::2] = True    # every other element, starting at 0
  odd_idx = ~even_idx
  # Assemble the complex conjugate roots in pairs.
  roots_cp = np.zeros( 2*cp_cj_pair_cnt, dtype=complex )
  roots_cp[even_idx] = roots_cp_tmp
  roots_cp[odd_idx] = roots_cp_cj


  # System's real roots and residuals random selection.
  roots_r = random_in_range( rt_re_rng[0], rt_re_rng[1], re_rt_cnt )

  # Insert the complete sets of roots.
  roots = np.concatenate( ( roots_r, roots_cp ) )

  return roots

def random_fitted_re_rat_func( num_cnt = 6, denom_cnt = 6, num_rng=(-1,1), 
  poles_re_rng=(-1,1), poles_im_rng=(-1,1), x_rng=(0,2), y_adj_amp=1 ):
  '''
  Specialized function which generates a lambda function that is based on the
  quotient between two randomly generated polynomials.
  
  There are a few key points that differentiate this rational function generator from being
  truly random:
    - The rational function will be strictly real.
    - The numerator polynomial is randomized based on coefficients, but the 
      denominator polynomial is randomized based on roots (poles) in order
      to control singularity points that may appear over the x-axis.
    - The denominator polynomial will avoid having real poles at all cost over
      the effective range (x_rng) of the function. It will thus always try to
      create complex conjugate pair roots rather than purely real roots. This implies
      that the number of coefficients in the denominator polynomial will be forcibly
      changed into an even number (rounded up).
    - The rational function will take an extra fitting step where it is forced to scale
      with respect to the specified effective range (x_rng) over the y-range from 0 to y_adj_amp.
      This "normalization" is only conducted based on the effective range ONLY, so the 
      function most likely is not adjusted as intended outside this effective range.

  Args:
    num_cnt: Number of coefficients in the numerator polynomial (order = num_cnt - 1).
    denom_cnt: Number of coefficients in the denominator polynomial (order = denom_cnt - 1).
    num_rng: The range of allowed values in the numerator polynomial coefficients.
    poles_re_rng: The range of allowed real parts in the denominator polynomial roots.
    poles_im_rng: The range of allowed imaginary parts in the denominator polynomial roots.
      Note that a threahold prevents any value too close to 0.
    x_rng: The effective x-axis range, where the rational function is normalized w.r.t.
    y_adj_amp: The normalization target limit. Normalization is applied so that y values
      within the effective range x_rng are between [0, y_adj_amp] or [ y_adj_amp, 0 ] if
      y_adj_amp is negative.
  '''

  if y_adj_amp == 0:
    raise ValueError(f"y_adj_amp cannot be 0.")

  # Force the denominator polynomial to have even number of roots.
  if denom_cnt % 2 != 0:
    denom_cnt += 1

  # Randomly generate the set of numerical polynomial coefficients.
  num_coeff_arr = random_in_range( num_rng[0], num_rng[1], num_cnt )
  # Generate the corresponding numerator polynomial.
  num_poly = np.poly1d( num_coeff_arr )

  # Generate real polynomial roots (poles) set.
  denom_roots = random_re_poly_roots( denom_cnt, poles_re_rng, poles_im_rng, False, 1e-1 )
  # Generate the corresponding denominator polynomial.
  denom_coeff_arr = np.poly( denom_roots )
  denom_poly = np.poly1d( denom_coeff_arr )

  # Define the lambda representing the rational function inits raw state.
  func_raw = lambda x: num_poly(x)/denom_poly(x)



  '''
  Adjustment to the generated rational function.
  '''
  
  # The number of sample points.
  samp_cnt = 400
  # The sampling set.
  x_arr = np.linspace( x_rng[0], x_rng[1], samp_cnt )
  # The sample data.
  y_raw_arr = func_raw( x_arr )

  # Determine the function range over the effective range.
  y_raw_rng = ( min( y_raw_arr ), max( y_raw_arr ) )
  # The amplitude of the function over the effective range.
  y_raw_amp = y_raw_rng[1] - y_raw_rng[0]

  # Define the scaling factor for the rational function to reach the intended
  # amplitude over the effective range.
  y_scale_fact = y_adj_amp / y_raw_amp

  # Define the adjusted parameter domain variation rational function.
  func_adj = lambda x: ( func_raw(x) - y_raw_rng[0] ) * y_scale_fact

  return func_adj, num_poly, denom_poly

def convert_ReIm_to_cconj_format( tar_ReIm_vec, vec_cconj_map ):
  '''
  Convert the target real-imaginary format array of vectors to complex conjugate 
  format array of vectors.

  '''

  # Make sure we have a 2D np array.
  if( ( not isinstance( tar_ReIm_vec, np.ndarray) ) or tar_ReIm_vec.ndim > 2 ):
    print( "Error: argument must be a 2D np array", file=sys.stderr )
    return np.array( [] )

  if( tar_ReIm_vec.ndim == 1 ):
    return convert_ReIm_to_cconj_format_vec( tar_ReIm_vec, vec_cconj_map )

  # Number of rows.
  row_cnt = tar_ReIm_vec.shape[0]
  col_cnt = tar_ReIm_vec.shape[1]


  ans_cplx = np.zeros( ( row_cnt, col_cnt ), dtype = complex )

  # Reconfigure pole and residue arrays so they are stored as real and imag parts rather than
  # complex values.
  for i in range( row_cnt ):
      
    cplx_vec_i = convert_ReIm_to_cconj_format_vec( tar_ReIm_vec[i,:], vec_cconj_map[i,:] )
    ans_cplx[i,:] = cplx_vec_i

  return ans_cplx

def convert_ReIm_to_cconj_format_vec( tar_ReIm_vec, vec_cconj_map ):
  '''
  Convert the target real-imaginary format vector to complex conjugate format vector.
  
  Args:
    tar_ReIm_vec: 
      Contains either real values of either purely real entries or real and imaginary pairs of complex conjugate entries. 
      Complex conjugate pair's real and imaginary parts MUST be placed one after each other.
    vec_cconj_map: 
      boolean vector of equal length as tar_vec indicating whether the entry is part of complex conjugate pair.
  
  Return:

  '''
  # Define numerical floor.
  tol = 1e-12

  # Obtain length of the vector.
  vec_len = len( tar_ReIm_vec )

  # Define array with just real and imaginary part magnitudes.
  vec = np.zeros( vec_len, dtype=complex )
  
  # Define flag indicating previous encounter with complex value.
  cconj_flag = False
  for z in range( vec_len ):

    # Skip current term if it is part of previous complex conjugate pair.
    if cconj_flag:
      cconj_flag = False
      continue

    # Current value real part.
    val_real_z = tar_ReIm_vec[z]

    # Current value imaginary part if cconj.
    if vec_cconj_map[z]:

      val_imag_z = tar_ReIm_vec[z+1]
      vec[z] = val_real_z + val_imag_z * 1j
      vec[z+1] = val_real_z - val_imag_z * 1j

      cconj_flag = True

    else:
       
      vec[z] = val_real_z + 0j


  return vec
  
def convert_cconj_to_ReIm_format( tar_vec ):

  # Make sure we have a 2D np array.
  if( ( not isinstance(tar_vec, np.ndarray) ) or tar_vec.ndim > 2 ):
    print( "Error: argument must be a 2D np array", file=sys.stderr )
    return np.array( [] )

  if( tar_vec.ndim == 1 ):
     return convert_cconj_to_ReIm_format_vec( tar_vec )

  # Number of rows.
  row_cnt = tar_vec.shape[0]
  col_cnt = tar_vec.shape[1]

  # Real-Imaginary format 2D array initialization.
  ans_ReIm = np.zeros( ( row_cnt, col_cnt ), dtype=float )
  ans_cconj_map = np.zeros( ( row_cnt, col_cnt ), dtype=bool )

  # Reconfigure pole and residue arrays so they are stored as real and imag parts rather than
  # complex values.
  for i in range( row_cnt ):
      
    ReIm_i, cconj_map_i = convert_cconj_to_ReIm_format_vec( tar_vec[i,:] )
    ans_ReIm[i,:] = ReIm_i
    ans_cconj_map[i,:] = cconj_map_i

  return ans_ReIm, ans_cconj_map

def convert_cconj_to_ReIm_format_vec( tar_vec ):
  '''
  Convert the target complex conjugate vector set to the real-imaginary format.
  
  Args:
    tar_vec:
    - Contains either purely real values or complex conjugate pairs. 
    - Complex conjugate pairs MUST be placed one after each other.
    - The first item of a complex conjugate pair is the one whose real and 
      imaginary parts will be saved to represent the both of them.
  
  Return:

  '''

  # Make sure we have a 2D np array.
  if( ( not isinstance(tar_vec, np.ndarray) ) or tar_vec.ndim != 1 ):
      print( "Error: argument must be a 1D np array", file=sys.stderr )
      return np.array( [] )

  # Define numerical floor.
  tol = 1e-12

  # Obtain length of the vector.
  vec_len = len( tar_vec )

  # Define array with just real and imaginary part magnitudes.
  vec_mag_arr = np.zeros( vec_len, dtype=float )
  # Define array to keep track which entries are part of a complex conjugate pair.
  vec_cconj_map = np.zeros( vec_len, dtype=bool )

  # Define flag indicating previous encounter with complex value.
  cconj_flag = False
  for z in range( vec_len ):

    # Skip current term if it is part of previous complex conjugate pair.
    if cconj_flag:
      cconj_flag = False
      continue

    # Current value.
    val_z = tar_vec[z]

    # Save real part.
    vec_mag_arr[z] = val_z.real

    # Complex conjugate values case.
    if( abs( val_z.imag ) > tol ):

      # Save imaginary part.
      vec_mag_arr[z+1] = val_z.imag
      # Pole complex conjugacy map update.
      vec_cconj_map[z] = True
      vec_cconj_map[z+1] = True

      cconj_flag = True

  return vec_mag_arr, vec_cconj_map
