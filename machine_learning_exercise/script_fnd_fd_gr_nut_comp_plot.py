'''
This script plots the target nutrient of the foundation foods from
the 5 food groups on a scatter plot to compare presence of the nutrient
in each food group.
'''



import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import foodDataParser as fdPar
from foodDataParser import food
from toolbox import indexingUtils as idxUtils


parser = fdPar.foodDataParser()

# This file's directory location shall be the root of all other relative pathing
# defined here.
dirName = os.path.dirname(__file__)


# ======================================================================= >>>>>
#   Food List Initialization
# ======================================================================= >>>>>

# Food ID initialization files.
init_file_names = [None]*5
init_file_names[0] = f"{dirName}\\ML_init_files\\init_food_fruits.csv"
init_file_names[1] = f"{dirName}\\ML_init_files\\init_food_vegetables.csv"
init_file_names[2] = f"{dirName}\\ML_init_files\\init_food_grains.csv"
init_file_names[3] = f"{dirName}\\ML_init_files\\init_food_proteinFoods.csv"
init_file_names[4] = f"{dirName}\\ML_init_files\\init_food_dairy.csv"  


# fdc_id_arr = np.zeros(0)
# for z in range( len(init_file_names) ):

#     # Obtain the array of food indices.
#     data_z = pd.read_csv( init_file_names[z] )
#     fdc_id_arr_z = data_z['fdc_id'].to_numpy()

#     # Append the current food index array and its corresponding value array to the full group.
#     fdc_id_arr = np.append( fdc_id_arr, fdc_id_arr_z )


data_z = pd.read_csv( init_file_names[0] )
fdc_id_fruit_arr = data_z['fdc_id'].to_numpy()
data_z = pd.read_csv( init_file_names[1] )
fdc_id_veg_arr = data_z['fdc_id'].to_numpy()
data_z = pd.read_csv( init_file_names[2] )
fdc_id_grain_arr = data_z['fdc_id'].to_numpy()
data_z = pd.read_csv( init_file_names[3] )
fdc_id_protein_arr = data_z['fdc_id'].to_numpy()
data_z = pd.read_csv( init_file_names[4] )
fdc_id_dairy_arr = data_z['fdc_id'].to_numpy()



nut_id_preset = food.get_preset_nut_id( preset_id = 0 )
# Print one example food nutritions.
tmp = parser.findFood_nutrients( fdc_id = fdc_id_veg_arr[0] )
print( tmp )
nut_tmp = tmp.get_nutrients( nut_id_list = nut_id_preset )
print( nut_tmp )



val_fruit = parser.find_fd_gr_nut( fdc_id_arr = fdc_id_fruit_arr, \
    nut_id_list = nut_id_preset )
val_veg = parser.find_fd_gr_nut( fdc_id_arr = fdc_id_veg_arr, \
    nut_id_list = nut_id_preset )
val_grain = parser.find_fd_gr_nut( fdc_id_arr = fdc_id_grain_arr, \
    nut_id_list = nut_id_preset )
val_protein = parser.find_fd_gr_nut( fdc_id_arr = fdc_id_protein_arr, \
    nut_id_list = nut_id_preset )
val_dairy = parser.find_fd_gr_nut( fdc_id_arr = fdc_id_dairy_arr, \
    nut_id_list = nut_id_preset )

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#   Target Nutrient Presence in Food Group Plot
# ======================================================================= >>>>>

# Select the nutrion id.
# nut_id_z = 30

for nut_id_z in range( nut_id_preset.size ):

    val_fruit_z = val_fruit[ :, nut_id_z ]
    x_fruit = [1]*len( val_fruit_z )
    # Create scatter plot
    plt.scatter( x_fruit, val_fruit_z, c = 'r', label = 'Fruits' )

    val_veg_z = val_veg[ :, nut_id_z ]
    x_veg = [2]*len( val_veg_z )
    # Create scatter plot
    plt.scatter( x_veg, val_veg_z, c = 'b', label = 'Vegs' )

    val_grain_z = val_grain[ :, nut_id_z ]
    x_grain = [3]*len( val_grain_z )
    # Create scatter plot
    plt.scatter( x_grain, val_grain_z, c = 'g', label = 'Grain' )

    val_protein_z = val_protein[ :, nut_id_z ]
    x_protein = [4]*len( val_protein_z )
    # Create scatter plot
    plt.scatter( x_protein, val_protein_z, c = 'y', label = 'Protein' )

    val_dairy_z = val_dairy[ :, nut_id_z ]
    x_dairy = [5]*len( val_dairy_z )
    # Create scatter plot
    plt.scatter( x_dairy, val_dairy_z, c = 'black', label = 'Dairy' )

    nut_name_arr = parser.getNutrName( nut_id_preset[nut_id_z] )
    nut_name = nut_name_arr[0]
    nut_unit_arr = parser.getNutrUnit( nut_id_preset[nut_id_z] )
    nut_unit = nut_unit_arr[0]

    # Set x-axis display range.
    plt.xlim(-1, 8)
    # Add titles and labels
    plt.title( f"[{nut_name}] (ID: {nut_id_preset[nut_id_z]}) Distribution Per Food Group" )
    plt.xlabel("X-axis")
    plt.ylabel(f"{nut_unit}")
    # Add a legend
    plt.legend()


    tmp = f"{currentdir}/plt_plots/{nut_id_preset[nut_id_z]}"
    plt.savefig( tmp )

    # Clear the current plot.
    plt.clf()



# Show plot
# plt.show()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#   Food Check
# ======================================================================= >>>>>



# for z in range( len( fdc_id_arr ) ):
#     tmp = parser.findFood_nutrients( fdc_id = fdc_id_arr[z] )
#     print( tmp )
#     nut_tmp = tmp.get_nutrients( nut_id_list = nut_id_preset )
#     print( nut_tmp )

#     lol = 0

# ======================================================================= <<<<<



# # Create scatter plot
# plt.scatter(x, y)
