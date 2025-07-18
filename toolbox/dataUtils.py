


import numpy as np

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
    



