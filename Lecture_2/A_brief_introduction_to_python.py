'''
STRINGS
'''
# creating
a = 'hello'     # can use single or double quotes
print(a)
type(a)

# slicing
a[0]        # returns 'h' (works like list slicing)
a[1:3]      # returns 'el'
a[-1]       # returns 'o'

# concatenating
a + ' there'        # use plus sign to combine strings
5 + ' there'        # error because they are different types
str(5) + ' there'   # cast 5 to a string in order for this to work
type(a)
type(5)
# How about?
5*a

# Quotes: single double and tripple
SingleQuote = 'Hi!'
DoubleQuote = "And I say 'Hi!'"
TripleQuote = '''Say,
"I’m in!"
This is line 3'''
print(SingleQuote)
print(DoubleQuote)
print(TripleQuote)

# Escape Codes: A back slash is a way to scpae the literal meaning of a character
# The end of line \n scape character 
print(’anbnnc’)
print(’a\nb\n\nc’)
# Escaping single quotes within a quote

# The double quote above can also be written as to give the same result:
# what would happen next?
print('And I say 'Hi!'')
# What would happen now?
print('And I say \'Hi!\'')
print("And I say 'Hi!'")

# checking length
len(a)      # returns 5 (number of characters)

# uppercasing
a[0] = 'H'      # error because strings are immutable (can't overwrite characters)
a.upper()       # string method (this method doesn't exist for lists)
a
b = a.upper()
b
b.lower()
b

# Counting character of--and within--a string
tale = 'This is the best of times.'
tale.count('i')

# String Indexes
test_str = 'Real Madrid at Barcelona'
test_str[15]
test_str[1:10]
test_str[1:10:1]
test_str[1:10:2]
# Let's say that you want to know what is the last character of a very long string
# but you do not know how long is the string to enter the right index.. do this!
test_str[-1]
test_str[5:-1]
# A special trick from this notation
test_str[::-1]

# Finding the location where a string begins
test_str.find(' at')
test_str[:test_str.find(' at')]   # 'Real Madrid'
test_str[test_str.find(' at'):]

# Split and join strings
tale = 'This is the best of times.'
taleList = tale.split()
newTale = '&'.join(taleList)
newTale.split('&')
'''
LISTS
'''
# creating
a = [1, 2, 3, 4, 5]     # create lists using brackets

# slicing
a[0]        # returns 1 (Python is zero indexed)
a[1:3]      # returns [2, 3] (inclusive of first index but exclusive of second)
a[-1]       # returns 5 (last element)

# appending
a[5] = 6        # error because you can't assign outside the existing range
a.append(6)     # list method that appends 6 to the end
a = a + [7]     # use plus sign to combine lists

# sorting
sorted(a)               # sorts the list
sorted(a, reverse=True) # reverse=True is an 'optional argument'
sorted(a, True)         # error because optional arguments must be named

# checking type
type(a)     # returns list
type(a[0])  # returns int

# checking length
len(a)      # returns 7

'''
FOR LOOPS AND LIST COMPREHENSIONS
'''
# for loop to print 1 through 5
nums = range(1, 6)      # create a list of 1 through 5
for num in nums:        # num 'becomes' each list element for one loop
    print num

# for loop to print 1, 3, 5
other = [1, 3, 5]       # create a different list
for x in other:         # name 'x' does not matter
    print x             # this loop only executes 3 times (not 5)

# for loop to create a list of cubes of 1 through 5
cubes = []                  # create empty list to store results
for num in nums:            # loop through nums (will execute 5 times)
    cubes.append(num**3)    # append the cube of the current value of num

# equivalent list comprehension
cubes = [num**3 for num in nums]    # expression (num**3) goes first, brackets
                                    # indicate we are storing results in a list

'''
EXERCISE:

1. Given that: letters = ['a','b','c']
Write a list comprehension that returns: ['A','B','C']
'''
letters = ['a', 'b', 'c']
[letter.upper() for letter in letters]  # iterate through a list of strings,
                                        # and each string has an 'upper' method
'''
2. Given that: word = 'abc'
Write a list comprehension that returns: ['A','B','C']
'''
word = 'abc'
[letter.upper() for letter in word]     # iterate through each character

'''
CONDITINALS
'''
temperature = 75
if temperature > 70:
    print('Wear shorts.')
else:
    print('Wear long pants.')
    print('Get some exercise outside.')
'''
DICTIONARIES

dictionaries are similar to lists:
- both can contain multiple data types
- both are iterable
- both are mutable

dictionaries are different from lists:
- dictionaries are unordered
- dictionary lookup time is constant regardless of dictionary size

dictionaries are like real dictionaries:
- dictionaries are made of key-value pairs (word and definition)
- dictionary keys must be unique (each word is only defined once)
- you can use the key to look up the value, but not the other way around
'''

# create a dictionary
family = {'dad':'Homer', 'mom':'Marge', 'size':2}

# examine a dictionary
family[0]           # error because there is no ordering
family['dad']       # returns 'Homer' (use a key to look up a value)
len(family)         # returns 3 (number of key-value pairs)
family.keys()       # returns list: ['dad', 'mom', 'size']
family.values()     # returns list: ['Homer', 'Marge', 2]
family.items()      # returns list of tuples:
                    #   [('dad', 'Homer'), ('mom', 'Marge'), ('size', 2)]

# modify a dictionary
family['cat'] = 'snowball'          # add a new entry
family['cat'] = 'snowball ii'       # edit an existing entry
del family['cat']                   # delete an entry
family['kids'] = ['bart', 'lisa']   # value can be a list

# accessing a list element within a dictionary
family['kids'][0]   # returns 'bart'

'''
EXERCISE:
1. Print the name of the mom.'''
family['mom']                       # returns 'Marge'
'''2. Change the size to 5.'''
family['size'] = 5                  # replaces existing value for 'size'
'''3. Add 'Maggie' to the list of kids.'''
family['kids'].append('Maggie')     # access a list, then append 'Maggie' to it
'''4. Fix 'bart' and 'lisa' so that the first letter is capitalized.'''
family['kids'][0] = 'Bart'          # capitalize names by overwriting them
family['kids'][1] = 'Lisa'

# or, capitalize using a list comprehension and the 'capitalize' string method
family['kids'] = [kid.capitalize() for kid in family['kids']]

# or, slice the string, uppercase the first letter, and concatenate with other letters
family['kids'] = [kid[0].upper()+kid[1:] for kid in family['kids']]
