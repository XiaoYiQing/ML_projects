


# ======================================================================= >>>>>
#	Python Dates
# ======================================================================= >>>>>

# A date in Python is not a data type of its own, 
# but we can import a module named datetime to work with dates as date objects.

import datetime

x = datetime.datetime.now()
print(x)

# The datetime module has many methods to return information about the date object.
print(x.year)
print(x.strftime("%A"))

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Python Dates: Create Date Objects
# ======================================================================= >>>>>

# To create a date, we can use the datetime() class (constructor) of the datetime module.
# The datetime() class requires three parameters to create a date: year, month, day.

y = datetime.datetime(2020, 5, 17)
print(y)
# The datetime() class also takes parameters for time and timezone (hour, minute, second, microsecond, tzone), but they are optional, and has a default value of 0, (None for timezone).


# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	The strftime() Method
# ======================================================================= >>>>>
print()
# The datetime object has the strftime() method for formatting date objects into readable strings.
# strftime() takes one parameter, format, to specify the format of the returned string:
x = datetime.datetime(2018, 6, 1)
print(x.strftime("%B"))
print(x.strftime("%A"))
# There are a lot more formatting options that you can look up online.
# ======================================================================= <<<<<


