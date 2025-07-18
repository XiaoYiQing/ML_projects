



import os
import pandas as pd
import pprint
import numpy as np
from sklearn import linear_model

import foodDataParser as fdPar


parser = fdPar.foodDataParser()


'''
choice = 7
if choice == 1:
    # Broccoli, raw
    food_idx = 321900
elif choice == 2:
    # Chicken, broilers or fryers, drumstick, meat only, cooked, braised
    food_idx = 331897
elif choice == 3:
    # Chicken, broiler or fryers, breast, skinless, boneless, meat only, cooked, braised
    food_idx = 331960
elif choice == 4:
    # Nuts, almonds, dry roasted, with salt added
    food_idx = 323294
elif choice == 5:
    # Peaches, yellow, raw
    food_idx = 325430
elif choice == 6:
    # Oil, olive, extra virgin
    food_idx = 748608
elif choice == 7:
    # Tomatoes, grape, raw
    food_idx = 321360
else:
    print( "Unknow choice id." )
'''


# Set pandas options to display all rows and columns without abbreviation
pd.set_option('display.max_rows', None)

food_idx = 2258586

my_food = parser.findFood_nutrients( fdc_id = food_idx )
print( my_food )
print( my_food.df_nut )

#fd_df_nut = my_food.get_nutrients( format_id = 1 )
#print( fd_df_nut )









