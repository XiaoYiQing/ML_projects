



'''
Percentiles are used in statistics to give you a number that describes the value that a given percent of the values are lower than.
'''

import numpy

# ======================================================================= >>>>>
#	Percentiles
# ======================================================================= >>>>>

ages = [10,20,25,30]

# What is the 75. percentile? The answer is 43, meaning that 75% of the people are 43 or younger.

print( 'The ages list: ', end = '' )
print( ages )


perc_val = [ 15, 26, 45, 50, 70 ]

for perc_x in perc_val:
	x = numpy.percentile(ages, perc_x)
	str_var = f"ages {perc_x} percentile: {x}"
	print( str_var )

# Note that the percentile value is not necessarily an entry of the list.
# It most likely to be a float value in-between existing entries.

# ======================================================================= <<<<<





