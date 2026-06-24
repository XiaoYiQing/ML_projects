'''
Script where I save the image files from mnist into directory.

However, I discovered that this is costly (60k files), so I changed it
to save only a few. This is just to see if I can extract files.
'''


import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np

from PIL import Image

# Obtain the database mnist.It contains a training set of 60,000 images and a 
# test set of 10,000 images, each representing digits from 0 to 9.
from keras.datasets import mnist




# ======================================================================= >>>>>
#       mnist Image Save To File
# ======================================================================= >>>>>

# Define the directory in which the mnist figures are to be saved.
img_dir = currentdir + '/char_img_data/mnist'

# Obtain all the 0 to 9 image database.
(X_train, y_train), (X_test, y_test) = mnist.load_data()


digit_cnts = np.zeros(10) 

# for z in range( len( X_train ) ):
for z in range( 10 ):

    # Obtain current image and its label.
    imagez_z = X_train[z]
    label_z = y_train[z]

    # Increment the count of the target number.
    digit_cnts[label_z] += 1

    # Set the name of the figure file to be saved.
    img_z_filename = str( label_z ) + '_n' + str( int( digit_cnts[ label_z ] ) ) + '.png'

    # Specify the full path where the image will be saved
    file_path_z = os.path.join( img_dir, img_z_filename )

    # Convert the image to PIL format
    img_z = Image.fromarray(image_z)

    # Save the image
    img_z.save(file_path_z)

# ======================================================================= <<<<<
