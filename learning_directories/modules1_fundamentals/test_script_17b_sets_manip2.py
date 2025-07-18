
# ======================================================================= >>>>>
#	Join Sets
# ======================================================================= >>>>>

# The union() method returns a new set with all items from both sets.
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = set1.union(set2)
print(set3)


# The '|' operator performs the same action as the union() method.
# '|' is the OR logic operator.
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = set1 | set2
print(set3)

# All the joining methods and operators can be used to join multiple sets.
# When using a method, just add more sets in the parentheses, separated by commas:
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = {"John", "Elena"}
set4 = {"apple", "bananas", "cherry"}
myset = set1.union(set2, set3, set4)
print(myset)
myset = set1 | set2 | set3 |set4
print(myset)

# union() can be used to join a set with a tuple. The result is a set:
x = {"a", "b", "c"}
y = (1, 2, 3)
z = x.union(y)
print(z)
# This combination conversion DOES NOT work with the '|' operator.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Update Sets
# ======================================================================= >>>>>

# The update() method inserts all items from one set into another.
# The update() changes the original set, and does not return a new set.
set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}
set1.update(set2)
print(set1)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Intersection Sets
# ======================================================================= >>>>>

# The intersection() method will return a new set, that only contains the items that are present in both sets.
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1.intersection(set2)
print(set3)
# You can use the '&' operator instead of the intersection() method, and you will get the same result:
# '&' is the AND logic operator.
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1 & set2
print(set3)

# Note: The '&' operator only allows you to join sets with sets, and not with other data types like you can with the intersecton() method.

# The intersection_update() method will also keep ONLY the duplicates, but it will change the original set instead of returning a new set.
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set1.intersection_update(set2)
print(x)

# ======================================================================= <<<<<




