'''
Starting script where I regain my bearings on how to use everything.
'''


import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )



from toolbox import indexingUtils as idxUtils
from toolbox.dataUtils import zscore_normalize_features
from toolbox.dataUtils import minmax_normalize_features




