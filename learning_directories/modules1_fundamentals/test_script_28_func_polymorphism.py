


# ======================================================================= >>>>>
#	Polymorphism
# ======================================================================= >>>>>

'''
The word "polymorphism" means "many forms", and in programming it refers to methods/functions/operators with the same name that can be executed on many objects or classes.
'''


# For example, the function len() can be used on strings, lists, tuples, , dictionaries, etc.
x = "Hello World!"
print( len(x), end = ' ' )

mylist = [ 1, 2, 3, 4 ]
print( len(mylist), end = ' ' )

mytuple = ("apple", "banana", "cherry")
print( len(mytuple) )


# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Polymorphism: Class
# ======================================================================= >>>>>

'''
Polymorphism is often used in Class methods, where we can have multiple classes with the same method name.

For example, say we have three classes: Car, Boat, and Plane, and they all have a method called move():
'''

class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Drive!")

class Boat:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Sail!")

class Plane:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Fly!")

car1 = Car("Ford", "Mustang")       #Create a Car class
boat1 = Boat("Ibiza", "Touring 20") #Create a Boat class
plane1 = Plane("Boeing", "747")     #Create a Plane class

# Create a tuple of the three vehicles.
tmp = (car1, boat1, plane1)
# Execute the function move() defined in all three classes.
for x in tmp:
  x.move()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Polymorphism: Class Inheritance
# ======================================================================= >>>>>

# Polymorphism still works through class inheritance. 
# Child classes sharing the same parent class all have access to the same function defined in the parent class, which means polymorphism of this function is automatically applied across all these child classes.

# The child classes may override this function, but this doesn't change the fact the child class has access to this function by the same name, and thus polymorphism is unaffected, though outcome of the function by this child class may differ from the other child classes.

class Vehicle:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Move!")

class Car(Vehicle):
  pass

class Boat(Vehicle):
  def move(self):
    print("Sail!")

class Plane(Vehicle):
  def move(self):
    print("Fly!")

car1 = Car("Ford", "Mustang") #Create a Car object
boat1 = Boat("Ibiza", "Touring 20") #Create a Boat object
plane1 = Plane("Boeing", "747") #Create a Plane object

for x in (car1, boat1, plane1):
  print(x.brand, end = ' ')
  print(x.model, end = ' ')
  x.move()

# ======================================================================= <<<<<


