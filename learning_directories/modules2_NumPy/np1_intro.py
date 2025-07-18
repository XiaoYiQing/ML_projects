


'''
NumPy is a Python library used for working with arrays.

It also has functions for working in domain of linear algebra, 
fourier transform, and matrices.

NumPy was created in 2005 by Travis Oliphant. It is an open source project 
and you can use it freely.

NumPy stands for Numerical Python.
'''

'''
In Python we have lists that serve the purpose of arrays, 
but they are slow to process.

NumPy aims to provide an array object that is up to 50x faster than 
traditional Python lists.

The array object in NumPy is called ndarray, it provides a lot of supporting 
functions that make working with ndarray very easy.

Arrays are very frequently used in data science, where speed and resources 
are very important.
'''

'''
Why is NumPy Faster Than Lists?

NumPy arrays are stored at one continuous place in memory unlike lists, 
so processes can access and manipulate them very efficiently.

This behavior is called locality of reference in computer science.

This is the main reason why NumPy is faster than lists. 
Also it is optimized to work with latest CPU architectures.
'''

'''
Which Language is NumPy written in?
NumPy is a Python library and is written partially in Python, but most of 
the parts that require fast computation are written in C or C++.
'''

'''
Where is the NumPy Codebase?
The source code for NumPy is located at this github repository:
https://github.com/numpy/numpy
'''


# ======================================================================= >>>>>
#	Introduction Exercise
# ======================================================================= >>>>>

# NumPy is usually imported under the np alias.
import numpy as np


arr = np.array([1, 2, 3, 4, 5])

str_var = f"My np array: {arr}"
print(str_var)

str_var = f"NumPy Version: {np.__version__}"
print(str_var)

# ======================================================================= <<<<<




