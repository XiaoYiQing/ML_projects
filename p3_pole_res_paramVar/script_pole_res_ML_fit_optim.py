



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


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from func_depo import PoleResSyst_SISO
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
from toolbox.dataUtils import convert_cconj_to_ReIm_format
from toolbox.dataUtils import convert_ReIm_to_cconj_format
from toolbox.dataUtils import random_in_range
from toolbox.dataUtils import random_re_poly_roots



do_test = True
# Random single parameter parametrization test.
if do_test:

# ------------------------------------------------------------------ >>>>>
#       Initialization (Data and Control Variables)
# ------------------------------------------------------------------ >>>>>

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

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Initial Data Plot Assessment
# ------------------------------------------------------------------ >>>>>

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
        
# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Data Reformatting for ML Training
# ------------------------------------------------------------------ >>>>>

    # Define poles and residues arrays under real and imaginary part format.
    pole_mag_arr = np.zeros( ( p_cnt, poleRes_cnt ), dtype=float )
    res_mag_arr = np.zeros( ( p_cnt, poleRes_cnt ), dtype=float )
    # Define boolean map keeping track whether a value is complex conjugate or not.
    pole_cconj_map = np.zeros( ( p_cnt, poleRes_cnt ), dtype=bool )
    res_cconj_map = np.zeros( ( p_cnt, poleRes_cnt ), dtype=bool )

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
    # Create concatenated scaling vector.
    scale_tf = np.concatenate(( scale_p, scale_r ))
    
    # normalize (broadcast over rows).
    pole_mag_norm = pole_mag_arr / scale_p[np.newaxis, :]
    res_mag_norm = res_mag_arr / scale_r[np.newaxis, :]

    

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Training
# ------------------------------------------------------------------ >>>>>

    load_from_save = False
    save_dir = currentdir + '/ML_model_deposit'
    model_fullfilename = save_dir + '/script_pole_res_eq_test.keras'

    # if load_from_save:
    #     model = keras.models.load_model( model_fullfilename )

    do_train = True
    if do_train:

        # Arrange the parameter data into intended shape.
        X = p_arr.reshape(-1,1)
        # Add the residues data to the poles data as an extention along the rows.
        T = np.hstack( [ pole_mag_norm, res_mag_norm ] )

        # Subdivide the initial data into a training set and a testing set.
        Xtr, Xval, Ttr, Tval = train_test_split(X, T, test_size=0.4, random_state=0)

        alpha = 100.0
        def smooth_max_vector(abs_err, alpha=alpha):
            '''
            Function creates a smoothed average over each row if alpha is small or
            approaches the true max of each row as alpha increases.

            The function's purpose is to control how sharply the ML session is going to rely on
            case-by-case average error, max error, or a mid-point between both.

            Suggest alpha in the range [20, 200] for a error profiles mixture of varying degree.

            Args:
                abs_err: (batch, m) The error magnitude table (axis 0 = parameter)
                alpha: control factor (Large alpha -> row max, small alpha -> row soft average)
            '''

            return tf.reduce_logsumexp(alpha * abs_err, axis=1) / alpha

        # y_true_norm, y_pred_norm: normalized targets shape (batch, m)
        def smooth_max_loss_phys(y_true_norm, y_pred_norm):
            '''
            The loss function intended for the ML session.

            Rather than looking at the mse, we try to use the max error
            of each case as the guiding metric during the gradient descent.
            '''

            # Revert the normalization.
            y_true = y_true_norm * scale_tf
            y_pred = y_pred_norm * scale_tf
            # Compute error magnitude table.
            abs_err = tf.abs( y_true - y_pred )                     # (batch, m)
            # Compute smoothed out max/average of each case of the batch.
            per_sample_smax = smooth_max_vector( abs_err, alpha )     # (batch,)
            # Compute the average over the entire batch.
            return tf.reduce_mean(per_sample_smax)                  # scalar


        # Define the NN model structure.
        model = keras.Sequential([
            layers.Input(shape=(1,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(T.shape[1], activation='linear')
        ])
        model.compile(optimizer='adam', loss=smooth_max_loss_phys)
        model.fit(Xtr, Ttr, validation_data=(Xval, Tval), epochs=200, batch_size=32, verbose=1)

# ------------------------------------------------------------------ <<<<<

        T_eval = model.predict( Xval )
        print( Tval[10,:] - T_eval[10,:] )
        print( Tval[15,:] - T_eval[15,:] )
        print( Tval[50,:] - T_eval[50,:] )

# ------------------------------------------------------------------ >>>>>
#       Model Evaluation (Through Plots)
# ------------------------------------------------------------------ >>>>>

        # p_eval_cnt = T_eval.shape[0]

        # pole_mag_norm_appr = T_eval[:,0:poleRes_cnt]
        # res_mag_norm_appr = T_eval[:,poleRes_cnt:]

        # print( pole_mag_norm_appr[10,:] )
        # print( pole_mag_norm[10,:] )

        # # Normalization reversion.
        # pole_mag_appr = pole_mag_norm_appr * scale_p[np.newaxis, :]
        # res_mag_appr  = res_mag_norm_appr  * scale_r[np.newaxis, :]

        # pole_appr = np.zeros( ( p_eval_cnt, poleRes_cnt ), dtype = complex )
        # res_appr = np.zeros( ( p_eval_cnt, poleRes_cnt ), dtype = complex )
        # # Reconfigure pole and residue arrays so they are stored as real and imag parts rather than
        # # complex values.
        # for i in range( p_cnt ):
            
        #     pole_i = convert_ReIm_to_cconj_format( pole_mag_appr[i,:], pole_cconj_map[0,:] )
        #     pole_appr[i,:] = pole_i
    
        #     res_i = convert_ReIm_to_cconj_format( res_mag_appr[i,:], res_cconj_map[0,:] )
        #     res_appr[i,:] = res_i

        

        # print( pole_appr[10,:] )
        # print( pole_arr[10,:] )