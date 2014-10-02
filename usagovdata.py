'''
This is the code test when learning the course
Computational investing with the book Python for
Data Science.

Ref. Ch2 USA government data analysis example

@author: Alicia Wang
@date: 2 Oct 2014
'''

# Third pary import
import numpy as np
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt

# A 3rd Party module to convert json string into a 
# Python dictionary
import json

path = '../pydata-book/ch02/usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]

print records[1]

print records[0]['tz']

time_zones = [rec['tz'] for rec in records if 'tz' in rec]

print time_zones[:10]
print len(time_zones)

# collections is in the Python Standard Library
from collections import Counter

counts = Counter(time_zones)
print counts.most_common(10)

frame = DataFrame(records) # use DataFrame structure in pandas
# print frame
print frame['tz'][:10]
 
clean_tz = frame['tz'].fillna('Missing') # fill the NA with missing
clean_tz[clean_tz == ''] = 'Unknown' # replace the empty string with Unknown

tz_counts = clean_tz.value_counts()
print tz_counts[:10]

# tz_counts[:10].plot(kind = 'barh', rot = 0)
# plt.show()

print frame['a'][1]
print frame.a[1]
print 'Now we try to track the browser information'

results = Series([x.split()[0] for x in frame.a.dropna()])

print results[:5]
print results.value_counts()[:8]

cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe.a.str.contains('Windows'), 'Windows',  'Not Windows')

print operating_system[:10]

# Group the operating system information by time zones
by_tz_os = cframe.groupby(['tz', operating_system])

agg_counts = by_tz_os.size().unstack().fillna(0)

print agg_counts[:10]

indexer = agg_counts.sum(1).argsort()

print indexer[:10]

count_subset = agg_counts.take(indexer)[-10:]

print count_subset

# count_subset.plot(kind = 'barh', stacked = True)
# plt.show()

normed_subset = count_subset.div(count_subset.sum(1), axis = 0)

normed_subset.plot(kind = 'barh', stacked = True)
plt.show()
