


import numpy as np
import random as rd


def rand_samp( arr_len, samp_cnt ):
    '''
    Generate "samp_cnt" random indices for an iterable of the given length "arr_len".
    No repeated indices by default.
    '''

    if samp_cnt >= arr_len:
        return range(arr_len)

    rand_idx = rd.sample( range( 0, arr_len ), samp_cnt )
    rand_idx = np.array(rand_idx)
    rem_idx = [True]*arr_len
    rem_idx = np.array(rem_idx)
    rem_idx[rand_idx] = not rem_idx[rand_idx].all()

    return rand_idx, rem_idx


def gen_range_pair( range0, range1 ):

    total_cnt = len( range0 ) * len( range1 )
    rg_pair = np.array( [ [None]*2 ] * total_cnt )

    z = 0
    for rg0_z in range0:

        for rg1_z in range1:
            
            rg_pair[z,:] = [ rg0_z, rg1_z ]

            z = z + 1

    return rg_pair

def seq_lazy_caterer( n ):
    '''
    Return the lazy caterer's sequence, which involves adding an incrementing integer
    as we progress through the sequence, starting from number 1:
        1, 2, 4, 7, 11, ...
    Indexing within the sequence starts at index n = 0.
    '''
    seq = 1

    for z in range(1,n+1):

        seq = seq + z

    return seq



