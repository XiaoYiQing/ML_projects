


'''
By default Python have these data types:

    > strings - used to represent text data, the text is given under quote marks. 
        e.g. "ABCD"
    > integer - used to represent integer numbers. e.g. -1, -2, -3
    > float - used to represent real numbers. e.g. 1.2, 42.42
    > boolean - used to represent True or False.
    > complex - used to represent complex numbers. e.g. 1.0 + 2.0j, 1.5 + 2.5j
'''

'''
NumPy has some extra data types, and refer to data types with one character, 
like i for integers, u for unsigned integers etc.
Below is a list of all data types in NumPy and the characters used to represent them:
    i - integer
    b - boolean
    u - unsigned integer
    f - float
    c - complex float
    m - timedelta
    M - datetime
    O - object
    S - string
    U - unicode string
    V - fixed chunk of memory for other type ( void )
'''



# ======================================================================= >>>>>
#	Data Types
# ======================================================================= >>>>>

import numpy as np


arr = np.array([1, 2, 3, 4])
print(f"Default numerical data type: {arr.dtype}")


arr = np.array(['apple', 'banana', 'cherry'])
print(f"Array fo string data type: {arr.dtype}")
# <U6: I am not sure, but I think this means unicode string of 6 bytes or less.

# Creating Arrays With a Defined Data Type
# We use the array() function to create arrays, this function can take an 
# optional argument: dtype that allows us to define the expected data type 
# of the array elements:
arr = np.array([1, 2, 3, 4], dtype='S')
print(f"{arr} has data type: {arr.dtype}")

# For i, u, f, S and U we can define size as well (Number of bytes).
arr = np.array([1, 2, 3, 4], dtype='i4')    #Integer of 4 bytes.
print(f"{arr} has data type: {arr.dtype}")

'''
What if a Value Can Not Be Converted?
If a type is given in which elements can't be casted then NumPy will raise a 
ValueError.

ValueError: In Python ValueError is raised when the type of passed argument 
to a function is unexpected/incorrect.
'''
# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Converting Data Type on Existing Arrays
# ======================================================================= >>>>>

'''
The best way to change the data type of an existing array, is to make 
a copy of the array with the astype() method.

The astype() function creates a copy of the array, and allows you to 
specify the data type as a parameter.

The data type can be specified using a string, like 'f' for float, 
'i' for integer etc. or you can use the data type directly like float 
for float and int for integer.
'''

arr = np.array([1.1, 0.0, 3.6])
newarr = arr.astype('i')
# or newarr = arr.astype(int)
print( f"{arr} (dtype = {arr.dtype}) copied as an int array: {newarr} (dtype = {newarr.dtype})" )

newarr = arr.astype(bool)
print( f"{arr} (dtype = {arr.dtype}) copied as an bool array: {newarr} (dtype = {newarr.dtype})" )

# ======================================================================= <<<<<



