

import numpy as np
import random
import os

from PIL import Image

# Obtain the database mnist.It contains a training set of 60,000 images and a 
# test set of 10,000 images, each representing digits from 0 to 9.
from keras.datasets import mnist

from toolbox.indexingUtils import rand_samp


def random_in_range(x0, x1, n):
  return np.random.uniform(x0, x1, size=n)

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



def convert_cconj_to_ReIm_format( tar_vec ):
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

  # Define numerical floor.
  tol = 1e-12

  # Obtain length of the vector.
  vec_len = len( tar_vec )

  # Define array with just real and imaginary part magnitudes.
  pole_mag_arr = np.zeros( vec_len, dtype=float )
  # Define array to keep track which entries are part of a complex conjugate pair.
  pole_cconj_map = np.zeros( vec_len, dtype=bool )

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
    pole_mag_arr[z] = val_z.real

    # Complex conjugate values case.
    if( abs( val_z.imag ) > tol ):

      # Save imaginary part.
      pole_mag_arr[z+1] = val_z.imag
      # Pole complex conjugacy map update.
      pole_cconj_map[z] = True
      pole_cconj_map[z+1] = True

      cconj_flag = True

  return pole_mag_arr, pole_cconj_map


def get_mnist_tr_ts_sets( tr_set_indiv_size ):
  '''
  Generate a training and a testing data sets from the mnist data set.
  The mnist data set consists of greyscale 28 by 28 pixel images of the 
  digits 0 to 9. It already has a subdivision of training and testing sets,
  but this function provides you a subdivision of your desired size.

  Args:
    tr_set_indiv_size (int): The amount of images representing each of the 
      0 to 9 digits to be designated as part of the traning set. Remaining
      images in each digit becomes part of the testing set. For example, if
      tr_set_indiv_size = 100, then 100 randomly select images from each of the
      0, 1, ..., 9 digit's set will be part of the training set (training set 
      total size = 1000) and all remaining images become the testing set.

      This number is automatically capped by the absolute smallest digit batch size.

  Returns:
    Two dictionaries that has as labels the digits 0 to 9:

    - Training set X_tr ( X_tr[z] for z in [0,9] is np array of dimensions [ tr_set_indiv_size, 28, 28, 1 ] )

    - Testing set X_ts ( X_ts[z] for z in [0,9] is np array of dimensions [ remain digit cnt, 28, 28, 1 ] )

  '''

  # ===================================================================== >>>>>
  #       mnist Data Import
  # ===================================================================== >>>>>

  # Obtain all the 0 to 9 image database.
  (X_tr, y_tr), (X_ts, y_ts) = mnist.load_data()

  # Obtain the shapes of the training set data.
  X_tr_shape = X_tr.shape
  y_tr_shape = y_tr.shape
  # Obtain the shapes of the testing set data.
  X_ts_shape = X_ts.shape

  # Obtain the image dataset properties.
  tr_img_cnt = X_tr_shape[0]
  ts_img_cnt = X_ts_shape[0]
  img_height = X_tr_shape[1]
  img_width =  X_tr_shape[2]

  # Initialize a dictionary to store images by their label.
  digit_arrs_list = { label: [] for label in range(10) }

  # Counter of each digit from 0 to 9.
  digit_cnts = np.zeros(10) 

  # Distribute the training set images based on their label value.
  for z in range( tr_img_cnt ):

    label_z = y_tr[z]
    image_z = X_tr[z]
    digit_arrs_list[ label_z ].append( image_z )

    digit_cnts[ label_z ] += 1        # Count the numbers of digit

  # Distribute the testing set images based on their label value.
  for z in range( ts_img_cnt ):
      
    label_z = y_ts[z]
    image_z = X_ts[z]
    digit_arrs_list[ label_z ].append( image_z )

    digit_cnts[ label_z ] += 1        # Count the numbers of digit

  # Convert lists to np arrays and add an extra dimension for the channel if needed
  for label_z in digit_arrs_list:

    images_z = digit_arrs_list[label_z]
    # Adding the singular channel dimension and converting lists to np.array
    digit_arrs_list[ label_z ] = np.array(images_z).reshape(-1, img_height, img_width, 1)


  # Obtain the smallest digit batch size amongst the numbers from 0 to 9.
  min_digit_cnt = np.min( digit_cnts )

  # ===================================================================== <<<<<


  # ===================================================================== >>>>>
  #       mnist Training and Testing Data Sets Subdivision
  # ===================================================================== >>>>>

  # Define the number of image samples to retain from each digit's image array.
  subset_size = tr_set_indiv_size
  subset_size = min( subset_size, min_digit_cnt )

  # Initialize a dictionary to store training images by their label.
  digit_train_list = { label: [] for label in range(10) }
  # Initialize a dictionary to store test images by their label.
  digit_test_list = { label: [] for label in range(10) }


  for label_z in digit_arrs_list:

    # Obtain current digit's image array.
    img_arr_z = digit_arrs_list[label_z]

    # Generate a subset sampling set.
    samp_idx, rem_idx = rand_samp( len( img_arr_z ), subset_size )

    # Subdivide the whole set into the training and sampling sets according the 
    # the given random sampling indexing.
    digit_train_list[label_z] = img_arr_z[ samp_idx ]
    digit_test_list[label_z] = img_arr_z[ rem_idx ]


  return digit_train_list, digit_test_list

  # ===================================================================== <<<<<


def load_png_files_as_gs( folder, twoDSizes ):
    '''
    Extract the .png files from the target directory as grayscale files data.

    Args:
      folder (String): The directory where all .png files will be parsed.
    
      twoDSizes (Size 2 int array): The pixel dimensions to be applied to all images
        parsed from the target directory (height and width, in that order). The
        returned image data will all be results of upscaling/downscaling into
        the specified dimensions.

    Returns:

        Two np arrays:
    
        - img_arr ( np.array of size [ # of img.s, twoDSizes[0], twoDSizes[1], 1 ] )
          => The array of 2D greyscale image pixel data.

        - label_arr ( np.array of 1 dimension of # of img.s in size )
          => The array of labels of the associated images, which are just their original filename stems.
    '''

    img_arr = []
    label_arr = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):  # Or other image extension
            img_z = Image.open(os.path.join(folder, filename)).convert('L')  # Convert to grayscale
            img_z = img_z.resize(( twoDSizes[0],  twoDSizes[1] ))  # Resize images
            img_z_px_array = np.array(img_z) # Conversion into 2D pixel data array.
            img_arr.append( img_z_px_array ) # Add current image 2D array to the array of image datas.
            label_z_str = filename.split('.')[0]  # Extract filename stem.
            label_arr.append( label_z_str )

    return np.array(img_arr).reshape(-1, twoDSizes[0],  twoDSizes[1], 1), np.array(label_arr)


def load_png_as_gs_wt_num_labels( folder, twoDSizes ):
   
  '''
  Extract the .png files from the target directory as grayscale files data and 
  following labelling rule where the true label is the first string before the
  first underscore or space. 
  For example, image "1_12.png" is interpreted as having label value 1.
  As well, image "89 (2)" is interpreted as having label value 89.

  Args:
    folder (String): The directory where all .png files will be parsed.
  
    twoDSizes (Size 2 int array): The pixel dimensions to be applied to all images
      parsed from the target directory (height and width, in that order). The
      returned image data will all be results of upscaling/downscaling into
      the specified dimensions.

  Returns:

    Two np arrays:

    - img_arr ( np.array of size [ # of img.s, twoDSizes[0], twoDSizes[1], 1 ] )
      => The array of 2D greyscale image pixel data.

    - label_arr ( np.array of 1 dimension of # of img.s in size )
      => The array of labels of the associated images, which are just their original filename stems.
  '''

  img_arr = []
  label_arr = []
  for filename in os.listdir(folder):
    if filename.endswith(".png"):  # Or other image extension
      img_z = Image.open(os.path.join(folder, filename)).convert('L')  # Convert to grayscale
      img_z = img_z.resize(( twoDSizes[0],  twoDSizes[1] ))  # Resize images
      img_z_px_array = np.array(img_z) # Conversion into 2D pixel data array.
      img_arr.append( img_z_px_array ) # Add current image 2D array to the array of image datas.
      label_z_str = filename.split('.')[0]  # Extract filename stem.
      label_z_str = label_z_str.split('_')[0]  # Extract string before first underscore.
      label_z_str = label_z_str.split(' ')[0]  # Extract string before first space.
      label_arr.append( int( label_z_str ) )

  return np.array(img_arr).reshape(-1, twoDSizes[0],  twoDSizes[1], 1), np.array(label_arr)



# X_norm, X_mu, X_sigma = zscore_normalize_features(X_train)
def zscore_normalize_features(X):
    """
    computes  X, zcore normalized by column
    
    Args:
      X (ndarray (m,n))     : input data, m examples, n features
      
    Returns:
      X_norm (ndarray (m,n)): input normalized by column
      mu (ndarray (n,))     : mean of each feature
      sigma (ndarray (n,))  : standard deviation of each feature
    """
    # find the mean of each column/feature
    mu     = np.mean(X, axis=0)                 # mu will have shape (n,)
    # find the standard deviation of each column/feature
    sigma  = np.std(X, axis=0)                  # sigma will have shape (n,)
    # element-wise, subtract mu for that column from each example, divide by std for that column
    X_norm = (X - mu) / sigma      

    return (X_norm, mu, sigma)


def minmax_normalize_features(X):
    
    max = np.max( X, axis=0 )
    min = np.min( X, axis=0 )

    X_norm = ( X - min )/( max - min )

    return (X_norm, max, min)


def gen_train_cross_test_sets( X, y, trainPerc, crossPerc):
    '''
    Generate the training, the cross-validation, and the testing sets.
    '''

    # Obtain the total data count.
    dCnt = np.shape( X )[0]
    



