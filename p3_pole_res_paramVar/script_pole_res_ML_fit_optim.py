



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


from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
from func_depo import PoleResSyst_SISO
from func_depo import convert_cconj_to_ReIm_format
from func_depo import convert_ReIm_to_cconj_format
from func_depo import random_re_poly_roots
from toolbox.dataUtils import random_in_range
from toolbox.dataUtils import zscore_normalize_features

from toolbox.dataUtils import center_and_rescale
from toolbox.dataUtils import center_and_rescale_revert



# ======================================================================= >>>>>
#       relu Model Optimization
# ======================================================================= >>>>>

do_test = False
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

    # Obtain the number of sample abstract parameter points.
    p_cnt = 1000
    var_fact = 0.2

    # Use the reference system to create a full set of randomly generated pole-res 
    # systems created based on the reference system which has its poles and residues varying 
    # over a single abstract parameter using randomly generated rational functions.
    pole_orig, res_orig = PoleResSyst_SISO.gen_rand_1param_var( mySyst, var_fact, p_cnt )

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
        pole_arr_z = pole_orig[z,:]
        res_arr_z = res_orig[z,:]
        # Assign the current poles and residues to their system.
        syst_arr[z].poles = pole_arr_z
        syst_arr[z].residues = res_arr_z

    do_plots = False
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

    # Convert from complex to real-imaginary format poles and residues arrays.
    pole_ReIm_orig, pole_cconj_map = convert_cconj_to_ReIm_format( pole_orig )
    res_ReIm_orig, res_cconj_map = convert_cconj_to_ReIm_format( res_orig )

    # Compute the column wise maximum magnitude.
    scale_p = np.max( np.abs( pole_ReIm_orig ), axis = 0 )
    scale_r = np.max( np.abs( res_ReIm_orig ), axis = 0 )
    # For columns having 0 max magnitude, force the scaling factor to 1
    scale_p[ scale_p == 0 ] = 1.0
    scale_r[ scale_r == 0 ] = 1.0
    # Create concatenated scaling vector.
    scale_tf = np.concatenate(( scale_p, scale_r ))
    
    # normalize (broadcast over rows).
    pole_ReIm_norm_orig = pole_ReIm_orig / scale_p[np.newaxis, :]
    res_ReIm_norm_orig = res_ReIm_orig / scale_r[np.newaxis, :]

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
        T = np.hstack( [ pole_ReIm_norm_orig, res_ReIm_norm_orig ] )

        # Define specific number of entries for the training set.
        N_train = int(round(0.4 * p_cnt))   
        if N_train < 2:
            raise ValueError("Need at least 2 training points (endpoints).")

        # Create linear indexing array for the training set with guarantee 
        # inclusion of end points.
        train_idx = np.unique(
            np.concatenate((
                [0, p_cnt - 1],
                np.round(np.linspace(1, p_cnt - 2, max(0, N_train - 2))).astype(int)
            ))
        )
        # Obtain the index array for the validation set, which is all that remains
        # from the starting set after taking out the training set.
        val_idx = np.setdiff1d(np.arange(p_cnt), train_idx)

        # Define the official training and validation sets.
        Xtr, Ttr = X[train_idx], T[train_idx]
        Xval, Tval = X[val_idx], T[val_idx]

        alpha = 100.0
        def smooth_max_vector(abs_err, alpha=100):
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

            #TODO: Consider reverting scaling for cases where the original scale
            #   is catually higher than the normalized one (higher error magnitude).
            # Compute error magnitude table.
            abs_err = tf.abs( y_true_norm - y_pred_norm )                   # (batch, m)
            # Compute smoothed out max/average of each case of the batch.
            per_sample_smax = smooth_max_vector( abs_err, alpha )           # (batch,)
            # Compute the average over the entire batch.
            return tf.reduce_mean(per_sample_smax)                          # scalar


        # Define the NN model structure.
        model = keras.Sequential([
            layers.Input(shape=(1,)),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(T.shape[1], activation='linear')
        ])
        model.compile(optimizer='adam', loss=smooth_max_loss_phys)
        model.fit(Xtr, Ttr, validation_data=(Xval, Tval), epochs=250, batch_size=32, verbose=1)

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Error Evaluation (Normalized)
# ------------------------------------------------------------------ >>>>>

        T_eval = model.predict( X )

        # Separate the approximated poles and residues.
        pole_ReIm_norm_appr = T_eval[:,0:poleRes_cnt]
        res_ReIm_norm_appr = T_eval[:,poleRes_cnt:]
        
        # Compute the normalized error.
        pole_ReIm_norm_err = pole_ReIm_norm_orig - pole_ReIm_norm_appr
        res_ReIm_norm_err = res_ReIm_norm_orig - res_ReIm_norm_appr

        # column-wise RMS (real or complex-safe)
        pole_ReIm_norm_RMS_err = np.sqrt( np.mean( np.abs( pole_ReIm_norm_err )**2, axis=0 ) )
        res_ReIm_norm_RMS_err = np.sqrt( np.mean( np.abs( res_ReIm_norm_err )**2, axis=0 ) )

        print( "Normalized poles RMS error: \n", pole_ReIm_norm_RMS_err )
        print( "Normalized residues RMS error: \n", res_ReIm_norm_RMS_err )

        do_plot = False
        if do_plot:

            fig1, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            for z in range( poleRes_cnt ):
                ax1.plot( p_arr, abs( pole_ReIm_norm_err[:,z] ) )
                ax2.plot( p_arr, abs( res_ReIm_norm_err[:,z] ) )

            # Poles Error Magnitudes.
            ax1.set_title("Normalized Poles Error Magnitudes")
            ax1.set_xlabel("p")
            ax1.set_ylabel("Norm Pole Err Mag")
            ax1.grid( True, 'both' )

            # Poles Error Magnitudes.
            ax2.set_title("Normalized Residues Error Magnitudes")
            ax2.set_xlabel("p")
            ax2.set_ylabel("Norm Res Err Mag")
            ax2.grid( True, 'both' )

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Error Evaluation (Original Format)
# ------------------------------------------------------------------ >>>>>

        # Normalization reversion.
        pole_ReIm_appr = pole_ReIm_norm_appr * scale_p[np.newaxis, :]
        res_ReIm_appr  = res_ReIm_norm_appr  * scale_r[np.newaxis, :]

        # Compute the error.
        pole_ReIm_err = pole_ReIm_orig - pole_ReIm_appr
        res_ReIm_err = res_ReIm_orig - res_ReIm_appr

        # column-wise RMS (real or complex-safe)
        pole_ReIm_RMS_err = np.sqrt( np.mean( np.abs( pole_ReIm_err )**2, axis=0 ) )
        res_ReIm_RMS_err = np.sqrt( np.mean( np.abs( res_ReIm_err )**2, axis=0 ) )

        print( "Poles RMS error: \n", pole_ReIm_RMS_err )
        print( "Residues RMS error: \n", res_ReIm_RMS_err )

        do_plot = False
        # Poles and Residues real and imaginary parts error magnitude plot.
        if do_plot:

            fig1, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            for z in range( poleRes_cnt ):
                ax1.plot( p_arr, abs( pole_ReIm_err[:,z] ) )
                ax2.plot( p_arr, abs( res_ReIm_err[:,z] ) )

            # Poles Error Magnitudes.
            ax1.set_title("Poles Error Magnitudes")
            ax1.set_xlabel("p")
            ax1.set_ylabel("Pole Err Mag")
            ax1.grid( True, 'both' )

            # Poles Error Magnitudes.
            ax2.set_title("Residues Error Magnitudes")
            ax2.set_xlabel("p")
            ax2.set_ylabel("Res Err Mag")
            ax2.grid( True, 'both' )

        
            
# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Error Evaluation (Complex Poles and Residues)
# ------------------------------------------------------------------ >>>>>

        pole_appr = convert_ReIm_to_cconj_format( pole_ReIm_appr, pole_cconj_map )
        res_appr = convert_ReIm_to_cconj_format( res_ReIm_appr, res_cconj_map )

        do_plot = True
        # Poles magnitude and phase comparison.
        if do_plot:

            fig1, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            fig3, ax3 = plt.subplots()
            fig4, ax4 = plt.subplots()

            for z in range( poleRes_cnt ):
                
                line1, = ax1.plot( p_arr, abs( pole_orig[:,z] ), linewidth=1 )
                color_z = line1.get_color()
                ax1.plot( p_arr, abs( pole_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )
                
                ax2.plot( p_arr, np.angle( pole_orig[:,z] ), linewidth=1, color=color_z )
                ax2.plot( p_arr, np.angle( pole_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )

                line1, = ax3.plot( p_arr, abs( res_orig[:,z] ), linewidth=1 )
                color_z = line1.get_color()
                ax3.plot( p_arr, abs( res_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )
                
                ax4.plot( p_arr, np.angle( res_orig[:,z] ), linewidth=1, color=color_z )
                ax4.plot( p_arr, np.angle( res_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )

            # Poles Error Magnitudes.
            ax1.set_title("Poles Magnitudes")
            ax1.set_xlabel("p")
            ax1.set_ylabel("Pole Mag")
            ax1.grid( True, 'both' )

            # Poles Error Magnitudes.
            ax2.set_title("Poles Phases")
            ax2.set_xlabel("p")
            ax2.set_ylabel("Poles Phase")
            ax2.grid( True, 'both' )

            # Residues Error Magnitudes.
            ax3.set_title("Res Magnitudes")
            ax3.set_xlabel("p")
            ax3.set_ylabel("Res Mag")
            ax3.grid( True, 'both' )

            # Residues Error Phases.
            ax4.set_title("Res Phases")
            ax4.set_xlabel("p")
            ax4.set_ylabel("Res Phase")
            ax4.grid( True, 'both' )

# ------------------------------------------------------------------ <<<<<
# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       softplus Model Optimization
# ======================================================================= >>>>>


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

    # Obtain the number of sample abstract parameter points.
    p_cnt = 1000
    var_fact = 0.2

    # Use the reference system to create a full set of randomly generated pole-res 
    # systems created based on the reference system which has its poles and residues varying 
    # over a single abstract parameter using randomly generated rational functions.
    pole_orig, res_orig = PoleResSyst_SISO.gen_rand_1param_var( mySyst, var_fact, p_cnt )

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
        pole_arr_z = pole_orig[z,:]
        res_arr_z = res_orig[z,:]
        # Assign the current poles and residues to their system.
        syst_arr[z].poles = pole_arr_z
        syst_arr[z].residues = res_arr_z

    do_plots = False
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

    # Convert from complex to real-imaginary format poles and residues arrays.
    pole_ReIm_orig, pole_cconj_map = convert_cconj_to_ReIm_format( pole_orig )
    res_ReIm_orig, res_cconj_map = convert_cconj_to_ReIm_format( res_orig )

    # Obtain standardize parameter array.
    p_norm, p_mean, p_std = zscore_normalize_features( p_arr[:] )

    pole_ReIm_norm_orig_tmp, pole_ReIm_mean, pole_ReIm_scale = \
        center_and_rescale( pole_ReIm_orig )

    pole_ReIm_orig_B = center_and_rescale_revert( pole_ReIm_norm_orig_tmp, \
        pole_ReIm_mean, pole_ReIm_scale )

    # Compute the column wise maximum magnitude.
    scale_p = np.max( np.abs( pole_ReIm_orig ), axis = 0 )
    scale_r = np.max( np.abs( res_ReIm_orig ), axis = 0 )
    # For columns having 0 max magnitude, force the scaling factor to 1
    scale_p[ scale_p == 0 ] = 1.0
    scale_r[ scale_r == 0 ] = 1.0
    # Create concatenated scaling vector.
    scale_tf = np.concatenate(( scale_p, scale_r ))
    
    # normalize (broadcast over rows).
    pole_ReIm_norm_orig = pole_ReIm_orig / scale_p[np.newaxis, :]
    res_ReIm_norm_orig = res_ReIm_orig / scale_r[np.newaxis, :]

    do_plots = False
    # Normalize poles and residues real and imaginary part plot.
    if do_plots:

        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        for z in range( poleRes_cnt ):
            ax1.plot( p_arr, pole_ReIm_norm_orig[:,z] )
            ax2.plot( p_arr, res_ReIm_norm_orig[:,z] )

        ax1.set_title("Normalize Pole ReIm Plot")
        ax1.set_xlabel("p")
        ax1.set_ylabel("Pole ReIm")
        ax1.grid( True, 'both' )

        ax2.set_title("Normalize Residue ReIm Plot")
        ax2.set_xlabel("p")
        ax2.set_ylabel("Res ReIm")
        ax2.grid( True, 'both' )

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Training
# ------------------------------------------------------------------ >>>>>

    do_train = False
    if do_train:

        # Arrange the parameter data into intended shape.
        X = p_norm.reshape(-1,1)
        # Add the residues data to the poles data as an extention along the rows.
        T = np.hstack( [ pole_ReIm_norm_orig, res_ReIm_norm_orig ] )

        # Define specific number of entries for the training set.
        N_train = int(round(0.4 * p_cnt))   
        if N_train < 2:
            raise ValueError("Need at least 2 training points (endpoints).")

        # Create linear indexing array for the training set with guarantee 
        # inclusion of end points.
        train_idx = np.unique(
            np.concatenate((
                [0, p_cnt - 1],
                np.round(np.linspace(1, p_cnt - 2, max(0, N_train - 2))).astype(int)
            ))
        )
        # Obtain the index array for the validation set, which is all that remains
        # from the starting set after taking out the training set.
        val_idx = np.setdiff1d(np.arange(p_cnt), train_idx)

        # Define the official training and validation sets.
        Xtr, Ttr = X[train_idx], T[train_idx]
        Xval, Tval = X[val_idx], T[val_idx]

        alpha = 100.0
        def smooth_max_vector(abs_err, alpha=100):
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

            #TODO: Consider reverting scaling for cases where the original scale
            #   is catually higher than the normalized one (higher error magnitude).
            # y_true_phys = y_true_norm * scale_tf
            # y_pred_phys = y_pred_norm * scale_tf
            # abs_err = tf.abs( y_true_phys - y_pred_phys )
            # Compute error magnitude table.
            abs_err = tf.abs( y_true_norm - y_pred_norm )                   # (batch, m)
            # Compute smoothed out max/average of each case of the batch.
            per_sample_smax = smooth_max_vector( abs_err, alpha=alpha )           # (batch,)
            # Compute the average over the entire batch.
            return tf.reduce_mean(per_sample_smax)                          # scalar


        # Define the NN model structure.
        model = keras.Sequential([
            layers.Input(shape=(1,)),
            layers.Dense(64, activation='softplus'),
            layers.Dense(64, activation='softplus'),
            layers.Dense(T.shape[1], activation='linear')
        ])
        model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3),
            loss=smooth_max_loss_phys)

        # --- Callbacks ---
        cb = [
            keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6),
            keras.callbacks.EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True)
        ]

        # --- Train ---
        history = model.fit(Xtr, Ttr, validation_data=(Xval, Tval),
            epochs=300, batch_size=32, callbacks=cb, verbose=2)

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Error Evaluation (Normalized)
# ------------------------------------------------------------------ >>>>>

        T_eval = model.predict( X )

        # Separate the approximated poles and residues.
        pole_ReIm_norm_appr = T_eval[:,0:poleRes_cnt]
        res_ReIm_norm_appr = T_eval[:,poleRes_cnt:]
        
        # Compute the normalized error.
        pole_ReIm_norm_err = pole_ReIm_norm_orig - pole_ReIm_norm_appr
        res_ReIm_norm_err = res_ReIm_norm_orig - res_ReIm_norm_appr

        # column-wise RMS (real or complex-safe)
        pole_ReIm_norm_RMS_err = np.sqrt( np.mean( np.abs( pole_ReIm_norm_err )**2, axis=0 ) )
        res_ReIm_norm_RMS_err = np.sqrt( np.mean( np.abs( res_ReIm_norm_err )**2, axis=0 ) )

        print( "Normalized poles RMS error: \n", pole_ReIm_norm_RMS_err )
        print( "Normalized residues RMS error: \n", res_ReIm_norm_RMS_err )

        do_plot = False
        # Normalize pole and residue errors plot.
        if do_plot:

            fig1, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            for z in range( poleRes_cnt ):
                ax1.plot( p_norm, abs( pole_ReIm_norm_err[:,z] ) )
                ax2.plot( p_norm, abs( res_ReIm_norm_err[:,z] ) )

            # Poles Error Magnitudes.
            ax1.set_title("Normalized Poles Error Magnitudes")
            ax1.set_xlabel("p")
            ax1.set_ylabel("Norm Pole Err Mag")
            ax1.grid( True, 'both' )

            # Poles Error Magnitudes.
            ax2.set_title("Normalized Residues Error Magnitudes")
            ax2.set_xlabel("p")
            ax2.set_ylabel("Norm Res Err Mag")
            ax2.grid( True, 'both' )

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Error Evaluation (Original Format)
# ------------------------------------------------------------------ >>>>>

        # Normalization reversion.
        pole_ReIm_appr = pole_ReIm_norm_appr * scale_p[np.newaxis, :]
        res_ReIm_appr  = res_ReIm_norm_appr  * scale_r[np.newaxis, :]

        # Compute the error.
        pole_ReIm_err = pole_ReIm_orig - pole_ReIm_appr
        res_ReIm_err = res_ReIm_orig - res_ReIm_appr

        # column-wise RMS (real or complex-safe)
        pole_ReIm_RMS_err = np.sqrt( np.mean( np.abs( pole_ReIm_err )**2, axis=0 ) )
        res_ReIm_RMS_err = np.sqrt( np.mean( np.abs( res_ReIm_err )**2, axis=0 ) )

        print( "Poles RMS error: \n", pole_ReIm_RMS_err )
        print( "Residues RMS error: \n", res_ReIm_RMS_err )

        do_plot = False
        # Poles and Residues real and imaginary parts error magnitude plot.
        if do_plot:

            fig1, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            for z in range( poleRes_cnt ):
                ax1.plot( p_norm, abs( pole_ReIm_err[:,z] ) )
                ax2.plot( p_norm, abs( res_ReIm_err[:,z] ) )

            # Poles Error Magnitudes.
            ax1.set_title("Poles Error Magnitudes")
            ax1.set_xlabel("p")
            ax1.set_ylabel("Pole Err Mag")
            ax1.grid( True, 'both' )

            # Poles Error Magnitudes.
            ax2.set_title("Residues Error Magnitudes")
            ax2.set_xlabel("p")
            ax2.set_ylabel("Res Err Mag")
            ax2.grid( True, 'both' )

            
# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Error Evaluation (Complex Poles and Residues)
# ------------------------------------------------------------------ >>>>>

        pole_appr = convert_ReIm_to_cconj_format( pole_ReIm_appr, pole_cconj_map )
        res_appr = convert_ReIm_to_cconj_format( res_ReIm_appr, res_cconj_map )

        do_plot = True
        # Poles magnitude and phase comparison.
        if do_plot:

            fig1, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            fig3, ax3 = plt.subplots()
            fig4, ax4 = plt.subplots()

            for z in range( poleRes_cnt ):
                
                line1, = ax1.plot( p_norm, abs( pole_orig[:,z] ), linewidth=1 )
                color_z = line1.get_color()
                ax1.plot( p_norm, abs( pole_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )
                
                ax2.plot( p_norm, np.angle( pole_orig[:,z] ), linewidth=1, color=color_z )
                ax2.plot( p_norm, np.angle( pole_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )

                line1, = ax3.plot( p_norm, abs( res_orig[:,z] ), linewidth=1 )
                color_z = line1.get_color()
                ax3.plot( p_norm, abs( res_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )
                
                ax4.plot( p_norm, np.angle( res_orig[:,z] ), linewidth=1, color=color_z )
                ax4.plot( p_norm, np.angle( res_appr[:,z] ), linewidth=2, linestyle='--', \
                    color=color_z )

            # Poles Error Magnitudes.
            ax1.set_title("Poles Magnitudes")
            ax1.set_xlabel("p")
            ax1.set_ylabel("Pole Mag")
            ax1.grid( True, 'both' )

            # Poles Error Magnitudes.
            ax2.set_title("Poles Phases")
            ax2.set_xlabel("p")
            ax2.set_ylabel("Poles Phase")
            ax2.grid( True, 'both' )

            # Residues Error Magnitudes.
            ax3.set_title("Res Magnitudes")
            ax3.set_xlabel("p")
            ax3.set_ylabel("Res Mag")
            ax3.grid( True, 'both' )

            # Residues Error Phases.
            ax4.set_title("Res Phases")
            ax4.set_xlabel("p")
            ax4.set_ylabel("Res Phase")
            ax4.grid( True, 'both' )


# ======================================================================= <<<<<



if len( plt.get_fignums() ) > 0:
    plt.show()

