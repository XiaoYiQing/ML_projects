


'''
Standard deviation is a number that describes how spread out the values are.

A low standard deviation means that most of the numbers are close to the mean (average) value.

A high standard deviation means that the values are spread out over a wider range.

Standard Deviation is often represented by the symbol Sigma: σ

'''

import numpy


# ======================================================================= >>>>>
#	Standard Deviation
# ======================================================================= >>>>>

speed_A = [86,87,88,86,87,85,86]
speed_B = [32,111,138,28,59,77,97]

print( 'The speed_A list: ', end = '' )
print( speed_A )

print( 'The speed_B list: ', end = '' )
print( speed_B )

x = numpy.std(speed_A)
str_var = f"speed_A std_dev: {x}"
print( str_var )

x = numpy.std(speed_B)
str_var = f"speed_B std_dev: {x}"
print( str_var )

# ======================================================================= <<<<<


'''
Variance is another number that indicates how spread out the values are.

In fact, if you take the square root of the variance, you get the standard deviation!

Or the other way around, if you multiply the standard deviation by itself, you get the variance!

Variance is often represented by the symbol Sigma Squared: σ^2

'''

# ======================================================================= >>>>>
#	Variance
# ======================================================================= >>>>>

x = numpy.var(speed_A)
str_var = f"speed_A variance: {x}"
print( str_var )

x = numpy.var(speed_B)
str_var = f"speed_B variance: {x}"
print( str_var )

# ======================================================================= <<<<<

