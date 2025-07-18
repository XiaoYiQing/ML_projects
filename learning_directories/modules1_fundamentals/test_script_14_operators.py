


'''
Operators are used to perform operations on variables and values.

Python divides the operators in the following groups:
	> Arithmetic operators
	> Assignment operators
	> Comparison operators
	> Logical operators
	> Identity operators
	> Membership operators
	> Bitwise operators
'''


# ===== Arithmetic operators =====
#	+	Addition	x + y	
#	-	Subtraction	x - y	
#	*	Multiplication	x * y	
#	/	Division	x / y	
#	%	Modulus	x % y	
#	**	Exponentiation	x ** y	
#	//	Floor division	x // y

x = 15
y = 7
print( x//y )


# ===== Assignment operators =====
#	=	x = 5	x = 5	
#	+=	x += 3	x = x + 3	
#	-=	x -= 3	x = x - 3	
#	*=	x *= 3	x = x * 3	
#	/=	x /= 3	x = x / 3	
#	%=	x %= 3	x = x % 3	
#	//=	x //= 3	x = x // 3	
#	**=	x **= 3	x = x ** 3	
#	&=	x &= 3	x = x & 3	
#	|=	x |= 3	x = x | 3	
#	^=	x ^= 3	x = x ^ 3	
#	>>=	x >>= 3	x = x >> 3	
#	<<=	x <<= 3	x = x << 3


# ===== Comparison operators =====
#	==	Equal	x == y	
#	!=	Not equal	x != y	
#	>	Greater than	x > y	
#	<	Less than	x < y	
#	>=	Greater than or equal to	x >= y	
#	<=	Less than or equal to	x <= y


# ===== Logical operators =====
#	and 	Returns True if both statements are true		x < 5 and  x < 10	
#	or		Returns True if one of the statements is true	x < 5 or x < 4	
#	not		Reverse the result, returns False if the result is true	not(x < 5 and x < 10)


# ===== Identity Operators =====
x = "I like cheese"
y = "I like cheese"
z = "I Like cheese"
ans = x is y
print(ans)
ans = x is not z
print(ans)


# ===== Membership operators =====
#	in 		Returns True if a sequence with the specified value is present in the object		x in y	
#	not in	Returns True if a sequence with the specified value is not present in the object	x not in y


# ===== Bitwise operators =====
#	& 	AND	Sets each bit to 1 if both bits are 1	x & y	
#	|	OR	Sets each bit to 1 if one of two bits is 1	x | y	
#	^	XOR	Sets each bit to 1 if only one of two bits is 1	x ^ y	
#	~	NOT	Inverts all the bits	~x	
#	<<	Zero fill left shift	Shift left by pushing zeros in from the right and let the leftmost bits fall #	off	x << 2	
#	>>	Signed right shift	Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off	x >> 2





# Final note:
#	Operators have set precedence which determines which operator acts first.
#	However, you should really use parentheses to ensure the order you want.
