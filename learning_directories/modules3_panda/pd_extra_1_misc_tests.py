
import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )

import pandas as pd
from toolbox import pandasUtils as pdUtils

# data = {
#   "calories": [420, 380, 390],
#   "duration": [50, 45, 40]
# }

data = {
  "calories": [0, 0, 0],
  "duration": [1, 2, 3]
}

# Load data into a DataFrame object:
df = pd.DataFrame(data)

df_norm = pdUtils.norm_all_col( df, norm_sch_id = 1 )
print( df_norm )

