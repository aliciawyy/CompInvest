'''
Note of learning pandas

@author Alicia Wang
@date 4 oct 2014
'''

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

### Two main data structures in pandas
# - Series
# - DataFrame

## A _Series_ is a one-dimensional array-like object containing an
## array of data and an associated array of data labels, called
## _index_

# Series initialization
obj = Series([4, 7, -5, 3]) # default index
obj2 = Series([4, 7, -5, 3], index = ['a', 'b', 'c', 'd'])

# Series initialization by passing a Python dict
sdata = {'Ohio':35000, 'Texas':71000, 'Oregon':16000, 'Utah':5000}
obj3  = Series(sdata)

states = ['California', 'Oregon', 'Ohio', 'Texas']
obj4   = Series(sdata, index = states) # new Series will follow the
                                       # _index_ order

print obj.values
print obj.index

print obj2.index, obj2['a'], obj2.b
print obj2[['c', 'd']]

# numpy array operations are still valid for Series
print np.exp(obj2)

# Series canalso be considered as a fixed length, ordered list
print 'b' in obj2

# pandas has _isnull_ and _notnull_ to detect the missing data
print pd.isnull(obj4) # or obj4.isnull()

# Series can automatically align differently-indexed data in arithmetic 
# operations
print obj3 + obj4

# Both the Series object itself and its index have a _name_attribute
obj4.name = 'Population'
obj4.index.name = 'State'

## A _DataFrame_ represents a tabular, spreadsheet-like data structure 
## containing an ordered collection of columns, each can be a different 
## value type.
## A DataFrame has both a row and column _index_.

# Initialization from a dict of equal-length lists or numpy arrays
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year':  [2000, 2001, 2002, 2001, 2002],
        'pop':   [1.5, 1.7, 3.6, 2.4, 2.9]}
frame = DataFrame(data)

# Initialization from a nested dict of dicts format
pop = {'Nevada':{2001:2.4, 2002:2.9},
       'Ohio':{2000:1.5, 2001:1.7, 2002:3.6}}
frame3 = DataFrame(pop)

# To specify the order of columns
print DataFrame(data)
print DataFrame(data, columns = ['year', 'state', 'pop'])

frame2 = DataFrame(data, columns = ['year', 'state', 'pop', 'debt'],
                   index = ['one', 'two', 'three', 'four', 'five'])


# A column of a DataFrame can be retrieved as a Series
print frame2['pop']

# A row of a DataFrame can be retrieved by indicating the _ix_ indexing field
print frame2.ix['three']

# Get the columns' names and the rows' names
print frame2.columns, frame2.index

# Columns can be modified by assignment with a scalar or an array of values
frame2['debt'] = 16.5
frame2['debt'] = np.arange(5.)
# Columns can also be modified with a Series, the missing index will be assigned
# NaN automatically, even if there are values before
print frame2
val = Series([-1.2, -1.5, -1.7], index = ['two', 'four', 'five'])
frame2['debt'] = val
print frame2

# Assigning a column that doesn't exist
frame2['eastern'] = (frame2.state == 'Ohio')
print frame2

# Delete a column
del frame2['eastern']
print frame2

# Transport the result
print frame3
print frame3.T

# The index and columns of dataframe have their names
frame3.index.name = "year"
frame3.columns.name = "state"
print "names of index and of columns:\n", frame3
print "values of the dataframe\n", frame3.values

arr2D = np.array([[ 2.1, 1.5],[ 2.4,  1.7], [ 2.9,  3.6]])
print arr2D
frame4 = DataFrame(arr2D, index = ["one", "two", "three"])
print frame4
'''
This file contains the routine to compute the bollinger band.
'''
# -------------------------------------------------------
def main():

# -------------------------------------------------------
if __name__ == '__main__':
    main()