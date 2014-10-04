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

# To specify the order of columns
print DataFrame(data)
print DataFrame(data, columns = ['year', 'state', 'pop'])
print DataFrame(data, columns = ['year', 'state', 'pop', 'debt'],
                index = ['one', 'two', 'three', 'four', 'five'])

frame2 = DataFrame(data, columns = ['year', 'state', 'pop', 'debt'],
                   index = ['one', 'two', 'three', 'four', 'five'])

# A column of a DataFrame can be retrieved as a Series
print frame2['pop']

# A row of a DataFrame can be retrieved by indicating the _ix_ indexing field
print frame2.ix['three']

# Columns can be modified by assignment with a scalar or an array of values
frame2['debt'] = 16.5
frame2['debt'] = np.arange(5.)