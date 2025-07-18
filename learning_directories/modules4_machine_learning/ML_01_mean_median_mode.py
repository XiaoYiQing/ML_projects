


'''
Mean - The average value
Median - The mid point value
Mode - The most common value
'''


import numpy
from scipy import stats

# ======================================================================= >>>>>
#	Mean
# ======================================================================= >>>>>

speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]

print( 'The speed list: ', end = '' )
print( speed )

x = numpy.mean(speed)
str_var = f"Mean: {x}"
print( str_var )

x = numpy.median(speed)
str_var = f"Median: {x}"
print( str_var )

x = stats.mode(speed)
print( x )

# ======================================================================= <<<<<



