# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:26:18 2016
@author: noel
"""
########################################
# A brief introduction to numpy arrays #
########################################
# http://wiki.quantsoftware.org/index.php?title=Numpy_Tutorial_1
#
# Prereqs: Basic python. "import", built-in data types (numbers, lists, 
#          strings), range
#
# This short tutorial is mostly about introducing numpy arrays, how they're
# different from basic python lists/tuples, and the various ways you can
# manipulate them.  It's intended to be both a runnable python script, and
# a step by step tutorial. 
# This tutorial does NOT cover
# 	1) Installing numpy/dependencies. For that see 
#			http://docs.scipy.org/doc/numpy/user/install.html
#	2) Basic python. This includes getting, installing, running the python
#		interpreter, the basic python data types (strings, numbers, sequences),
#		if statements, or for loops. If you're new to python an excellent place
#		to start is here:
#			http://docs.python.org/2/tutorial/
#	3) Any numpy libraries in depth. It may include references to utility
#		functions where necessary, but this is strictly a tutorial for 
#		beginners. More advanced documentation is available here:
#			(Users guide)
#			http://docs.scipy.org/doc/numpy/user/index.html
#			(Reference documentation)
#			http://docs.scipy.org/doc/numpy/reference/
#March 26, 2016 340 to 285 lines
#
#
## Lets get started!
import numpy as np
import matplotlib.pyplot as plt 
## numpy array Filled with zeros:
zeroArray = np.zeros( (2,3) ) # [[ 0.  0.  0.]
print zeroArray               #  [ 0.  0.  0.]]
## Or ones:
oneArray = np.ones( (2,3) )   # [[ 1.  1.  1.]
print oneArray                #  [ 1.  1.  1.]]
## Or filled with junk:
emptyArray = np.empty( (2,3) ) 
print emptyArray
## Note, emptyArray might look random, but it's just uninitialized which means
## you shouldn't count on it having any particular data in it, even random
## data! If you do want random data you can use random():
randomArray = np.random.random( (2,3) )
print randomArray
## If you're following along and trying these commands out, you should have
## noticed that making randomArray took a lot longer than emptyArray. That's
## because np.random.random(...) is actually using a random number generator
## to fill in each of the spots in the array with a randomly sampled number
## from 0 to 1.
## You can also create an array by hand from a list of list:
foo = [ [1,2,3],
        [4,5,6]]
myArray = np.array(foo) # [[1 2 3] 
print myArray           #  [4 5 6]]
print "Reshaping arrays"
## Of course, if you're typing out a range for a larger matrix, it's easier to
## use arange(...):
rangeArray = np.arange(6,12).reshape( (2,3) ) # [[ 6  7  8]
print rangeArray                              #  [ 9 10 11]]
# there's two things going on here. First, the arange(...) function returns a 1D
# 1D array similar to what you'd get from using the built-in python function range(...) 
# with the same arguments, except it returns a numpy array instead of a list.
print np.arange(6,12) # [ 6  7  8  9 10 11 12]
## the reshape method takes the data in an existing array, and stuffs it into
## an array with the given shape and returns it.  
print rangeArray.reshape( (3,2) ) # [[ 6  7]
                                  #  [ 8  9]
                                  #  [10 11]]
#The original array doesn't change though.
print rangeArray # [[ 6  7  8]
                 #  [ 9 10 11]
## When you use reshape(...) the total number of things in the array must stay
## the same. So reshaping an array with 2 rows and 3 columns into one with 
## 3 rows and 2 columns is fine, but 3x3 or 1x5 won't work
#print rangeArray.reshape( (3,3) ) #ERROR
squareArray = np.arange(1,10).reshape( (3,3) ) #this is fine, 9 elements
print "Accessing array elements"
## Accessing an array is also pretty straight forward. You access a specific
## spot in the table by referring to its row and column inside square braces
## after the array:
print rangeArray[0,1] #7
## Note that row and column numbers start from 0, not 1! Numpy also lets you 
## refer to ranges inside an array:
print rangeArray[0,0:2] #[6 7]
print squareArray[0:2,0:2] #[[1 2]  # the top left corner of squareArray
                           # [4 5]]
## These ranges work just like slices and python lists. n:m:t specifies a range
## that starts at n, and stops before m, in steps of size t. If any of these 
## are left off, they're assumed to be the start, the end+1, and 1 respectively
print squareArray[:,0:3:2] #[[1 3]   #skip the middle column
                           # [4 6]
                           # [7 9]]
## Also like python lists, you can assign values to specific positions, or
## ranges of values to slices
squareArray[0,:] = np.array(range(1,4)) #set the first row to 1,2,3
squareArray[1,1] = 0                    # set the middle spot to zero
squareArray[2,:] = 1                    # set the last row to ones
print squareArray                       # [[1 2 3]
                                        #  [4 0 6]
                                        #  [1 1 1]]
## Something new to numpy arrays is indexing using an array of indices:
fibIndices = np.array( [1, 1, 2, 3] )
randomRow = np.random.random( (10,1) ) # an array of 10 random numbers
print randomRow
print randomRow[fibIndices] # the first, first, second and third element of
                             # randomRow 
## You can also use an array of true/false values to index:
boolIndices = np.array( [[ True, False,  True],
                          [False,  True, False],
                          [ True, False,  True]] )
print squareArray[boolIndices] # a 1D array with the selected values
                               # [1 3 0 1 1]
## It gets a little more complicated with 2D (and higher) arrays.  You need
## two index arrays for a 2D array:
rows = np.array( [[0,0],[2,2]] ) #get the corners of our square array
cols = np.array( [[0,2],[0,2]] )
print squareArray[rows,cols]     #[[1 3]
                                 # [1 1]]
boolRows = np.array( [False, True, False] ) # just the middle row
boolCols = np.array( [True, False, True] )  # Not the middle column
print squareArray[boolRows,boolCols]        # [4 6]
print "Operations on arrays"
## One useful trick is to create a boolean matrix based on some test and use
## that as an index in order to get the elements of a matrix that pass the
## test:
sqAverage = np.average(squareArray) # average(...) returns the average of all
                                    # the elements in the given array
betterThanAverage = squareArray > sqAverage
print betterThanAverage             #[[False False  True]
                                    # [ True False  True]
                                    # [False False False]]
print squareArray[betterThanAverage] #[3 4 6]
## Indexing like this can also be used to assign values to elements of the
## array. This is particularly useful if you want to filter an array, say by 
## making sure that all of its values are above/below a certain threshold:
sqStdDev = np.std(squareArray) # std(...) returns the standard deviation of
                               # all the elements in the given array
clampedSqArray = np.array(squareArray.copy(), dtype=float) 
                                    # make a copy of squareArray that will
                                    # be "clamped". It will only contain
                                    # values within one standard deviation
                                    # of the mean. Values that are too low
                                    # or to high will be set to the min
                                    # and max respectively. We set 
                                    # dtype=float because sqAverage
                                    # and sqStdDev are floating point
                                    # numbers, and we don't want to 
                                    # truncate them down to integers.
clampedSqArray[ (squareArray-sqAverage) > sqStdDev ] = sqAverage+sqStdDev
clampedSqArray[ (squareArray-sqAverage) < -sqStdDev ] = sqAverage-sqStdDev
print clampedSqArray # [[ 1.          2.          3.        ]
                     #  [ 3.90272394  0.31949828  3.90272394]
                     #  [ 1.          1.          1.        ]]


## Multiplying and dividing arrays by numbers does what you'd expect. It
## multiples/divides element-wise
print squareArray * 2 # [[ 2  4  6]
                      #  [ 8  0 12]
                      #  [ 2  2  2]]
## Addition works similarly:
print squareArray + np.ones( (3,3) ) #[[2 3 4]
                                     # [5 1 7]
                                     # [2 2 2]]
## Multiplying two arrays together (of the same size) is also element wise
print squareArray * np.arange(1,10).reshape( (3,3) ) #[[ 1  4  9]
                                                     # [16  0 36]
                                                     # [ 7  8  9]]
## Unless you use the dot(...) function, which does matrix multiplication
## from linear algebra:
matA = np.array( [[1,2],[3,4]] )
matB = np.array( [[5,6],[7,8]] )
print np.dot(matA,matB) #[[19 22]
                        # [43 50]]

## And thats it! There's a lot more to the numpy library, and there are a few
## things I skipped over here, such as what happens when array dimensions
## don't line up when you're indexing or multiplying them together, so if 
## you're interested, I strongly suggest you head over to the scipy wiki's
## numpy tutorial for a more in depth look at using numpy arrays:
##
##			http://www.scipy.org/Tentative_NumPy_Tutorial
###############################################################################
# 05_numpy.py
# create ndarrays from lists
# note: every element must be the same type (will be converted if possible)
data1 = [6, 7.5, 8, 0, 1]           # list
arr1 = np.array(data1)              # 1d array
data2 = [range(1, 5), range(5, 9)]  # list of lists
arr2 = np.array(data2)              # 2d array
arr2
arr2.tolist()                       # convert array back to list

# examining arrays
arr1.dtype      # float64
arr2.dtype      # int64
arr2.ndim       # 2
arr2.shape      # (2, 4) - axis 0 is rows, axis 1 is columns
arr2.size       # 8 - total number of elements
len(arr2)       # 2 - size of first dimension (aka axis)

# create special arrays
np.zeros(10)
np.zeros((3, 6))
np.ones(10)
np.linspace(0, 1, 5)            # 0 to 1 (inclusive) with 5 points
np.logspace(0, 3, 4)            # 10^0 to 10^3 (inclusive) with 4 points

# arange is like range, except it returns an array (not a list)
int_array = np.arange(5)
float_array = int_array.astype(float)

# slicing
arr1[0]         # 0th element (slices like a list)
arr2[0]         # row 0: returns 1d array ([1, 2, 3, 4])
arr2[0, 3]      # row 0, column 3: returns 4
arr2[0][3]      # alternative syntax
arr2[:, 0]      # all rows, column 0: returns 1d array ([1, 5])
arr2[:, 0:1]    # all rows, column 0: returns 2d array ([[1], [5]])

# views and copies
arr = np.arange(10)
arr[5:8]                    # returns [5, 6, 7]
arr[5:8] = 12               # all three values are overwritten (would give error on a list)
arr_view = arr[5:8]         # creates a "view" on arr, not a copy
arr_view[:] = 13            # modifies arr_view AND arr
arr_copy = arr[5:8].copy()  # makes a copy instead
arr_copy[:] = 14            # only modifies arr_copy

# using boolean arrays
names = np.array(['Bob', 'Joe', 'Will', 'Bob'])
names == 'Bob'                          # returns a boolean array
names[names != 'Bob']                   # logical selection
(names == 'Bob') | (names == 'Will')    # keywords "and/or" don't work with boolean arrays
names[names != 'Bob'] = 'Joe'           # assign based on a logical selection
np.unique(names)                        # set function
# vectorized operations
nums = np.arange(5)
nums*10                             # multiply each element by 10
nums = np.sqrt(nums)                # square root of each element
np.ceil(nums)                       # also floor, rint (round to nearest int)
np.isnan(nums)                      # checks for NaN
nums + np.arange(5)                 # add element-wise
np.maximum(nums, np.array([1, -2, 3, -4, 5]))  # compare element-wise
# math and stats
rnd = np.random.randn(4, 2) # random normals in 4x2 array
rnd.mean()
rnd.std()
rnd.argmin()                # index of minimum element
rnd.sum()
rnd.sum(axis=0)             # sum of columns
rnd.sum(axis=1)             # sum of rows
# use numpy to create scatter plots
N = 50
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area =30+(70*np.random.rand(N)) # 30 to 100 point radiuses
plt.scatter(x, y, s=area, c=colors,)
plt.show()
# conditional logic
np.where(rnd > 0, 2, -2)    # args: condition, value if True, value if False
np.where(rnd > 0, 2, rnd)   # any of the 3 arguments can be an array
# methods for boolean arrays
(rnd > 0).sum()             # counts number of positive values
(rnd > 0).any()             # checks if any value is True
(rnd > 0).all()             # checks if all values are True
# reshape, transpose, flatten
nums = np.arange(32).reshape(8, 4) # creates 8x4 array
nums.T                       # transpose
nums.flatten()               # flatten
# random numbers
np.random.seed(12234)
np.random.rand(2, 3)      # 0 to 1, in the given shape
np.random.randn(10)         # random normals (mean 0, sd 1)
np.random.randint(0, 2, 10) # 0 or 1
