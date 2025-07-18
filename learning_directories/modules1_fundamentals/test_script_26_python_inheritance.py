


'''
Inheritance allows us to define a class that inherits all the methods and properties from another class.

Parent class is the class being inherited from, also called base class.

Child class is the class that inherits from another class, also called derived class.
'''

# ======================================================================= >>>>>
#	Python Inheritance
# ======================================================================= >>>>>

# Here is our example parent class.
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

x = Person("John", "Doe")
x.printname()

# To create a class that inherits the functionality from another class, send the parent class as a parameter when creating the child class:
class Student(Person):
  pass

# Despite not having any object functions, the child class directly has access to the parent class functions.
x = Student("Mike", "Olsen")
x.printname()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Python Inheritance: __init__() Override
# ======================================================================= >>>>>

# When you add the __init__() function, 
#	the child class will no longer inherit the parent's __init__() function.

# Add the __init__() function to the Student class:
class Student(Person):
  def __init__(self, fname, lname):
    self.firstname = fname + '_studClass'
    self.lastname = lname + '_studClass'
x = Student("Mike", "Olsen")
x.printname()

# To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function:
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)
x = Student("Mike", "Olsen")
x.printname()
# This use of the parent class constructor now opens up the chance to add additional functionality in the __init__() function without discarding the original parent __init__() function.

# Python also has a super() function that will make the child class inherit all the methods and properties from its parent:
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
# Note:
#	 Person.__init__(self, fname, lname) does the same thing as super().__init__(fname, lname)
# The latter expression can be used for all child classes without having to write the class name of parent exactly.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Python Inheritance: Additional Functionalities
# ======================================================================= >>>>>

# Add properties and methods
class Student(Person):

	def __init__(self, fname, lname, year):
		super().__init__(fname, lname)
		self.graduationyear = year
		
	def welcome(self):
		print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

x = Student("Mike", "Olsen", 2019)
x.welcome()
# NOTE: If you add a method in the child class with the same name as a function in the parent class, 
# the inheritance of the parent method will be overridden.


# ======================================================================= <<<<<

