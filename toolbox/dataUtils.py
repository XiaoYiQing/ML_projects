

import numpy as np
import os

from PIL import Image

# Obtain the database mnist.It contains a training set of 60,000 images and a 
# test set of 10,000 images, each representing digits from 0 to 9.
from keras.datasets import mnist

from toolbox.indexingUtils import rand_samp

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
    



