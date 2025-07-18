


'''
An iterator is an object that contains a countable number of values.

An iterator is an object that can be iterated upon, meaning that you can traverse through all the values.

Technically, in Python, an iterator is an object which implements the iterator protocol, which consist of the methods __iter__() and __next__().
'''


# ======================================================================= >>>>>
#	Python Iterators
# ======================================================================= >>>>>

#Lists, tuples, dictionaries, and sets are all iterable objects. They are iterable containers which you can get an iterator from.

#All these objects have a iter() method which is used to get an iterator:
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)
x = next(myit)
print( x, end = ' ' )
x = next(myit)
print( x, end = ' ')
x = next(myit)
print( x, end = ' ')
print()

# Even strings are iterable objects, and can return an iterator:
mystr = "banana"
myit = iter(mystr)
for x in range(6):
	print( next(myit), end = ' ' )
print()

# Of course, you can just use the for loop to iterate through an iterable object:
for x in mystr:
	print( x, end = ' ' )
print()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Python Iterators: Creation
# ======================================================================= >>>>>

'''
To create an object/class as an iterator you have to implement the methods __iter__() and __next__() to your object.
These are not defined by default when you create a class.

The __iter__() method acts similar to __init__(), but must always return the iterator object itself.
The __next__() method must also return the next item in the sequence.
'''

class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in range(5):
	print( next(myiter), end = ' ' )
print()

# To prevent the iteration from going on forever, we can use the StopIteration statement, as implented above.
# In the __next__() method, the terminating condition raises an error if the iteration is done a specified number of times. This error does not stop the program, but ends the iteration loop.
for x in myiter:
  print( x, end = ' ' )
print()

# ======================================================================= <<<<<






