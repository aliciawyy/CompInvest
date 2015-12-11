"""
This is the code to learn QSTK

@author: Alicia Wang
@date: 3 Oct 2014
"""

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas.io.data
from scipy import stats

print "Pandas Version", pd.__version__

# def main():
''' Main Function'''

# List of symbols
ls_symbols = ["ML.PA", "LG.PA", "DG.PA", "^FCHI" ]  
ls_names   = ["Michelin", "Lafarge", "Vinci", "CAC 40"]

# Start and End date of the charts

dt_end   = dt.datetime.today()
dt_start = dt_end - dt.timedelta(days = 365)

ldf_data = pd.io.data.get_data_yahoo(ls_symbols,start=dt_start, end=dt_end)

for skey in ['Volume', 'Adj Close']:
    '''First forward fill then backward fill'''
    ldf_data[skey] = ldf_data[skey].fillna(method='ffill')
    ldf_data[skey] = ldf_data[skey].fillna(method='bfill')
    ldf_data[skey] = ldf_data[skey].fillna(1.0)

ls_volume = ldf_data['Volume'].values
ls_price  = ldf_data['Adj Close'].values

ls_date   = ldf_data['Adj Close'].index

plt.plot(ls_date, ls_price)
plt.legend(ls_names)
plt.ylabel('Adjusted Close')
plt.xlabel('Date')
plt.savefig('adjustedclose.pdf', format='pdf')

# Normalizing the prices to start at 1 and see relative returns
ls_normalized_price = ls_price / ls_price[0, :]
plt.clf()
plt.plot(ls_date, ls_normalized_price)
plt.legend(ls_names)
plt.ylabel('Normalized Close')
plt.xlabel('Date')
plt.savefig('normalized.pdf', format='pdf')

# Copy the normalized prices to a new ndarry to find returns.
ls_rets = ls_normalized_price.copy()

# Calculate the daily returns of the prices. (Inplace calculation)
# returnize0 works on ndarray and not dataframes.
tsu.returnize0(ls_rets)

# Plotting the plot of daily returns
plt.clf()
plt.plot(ls_date[0:100], ls_rets[0:100,0])
plt.plot(ls_date[0:100], ls_rets[0:100,3])
plt.legend([ls_names[0], ls_names[3]])
plt.axhline(y=0, color='r')
plt.ylabel('Daily Returns')
plt.xlabel('Date')
plt.savefig('rets.pdf', format='pdf')

# Some regression analysis on the dependency of the above stocks
nsize = len(ls_symbols) # number of stocks
slope  = np.zeros((nsize-1, nsize))
rvalue = np.zeros((nsize-1, nsize))
pvalue = np.zeros((nsize-1, nsize))

for i in range(0, nsize-1):
    for j in range (i+1, nsize):
        slope[i,j], intercept, rvalue[i,j], pvalue[i,j], std_err =\
            stats.linregress(ls_rets[:,i],ls_rets[:,j])
        
# Plotting the scatter plot of daily returns between two stocks
'''
plt.clf()
plt.scatter(ls_rets[:200, 1], ls_rets[:200, 3], c='blue')
plt.xlabel(ls_names[1])
plt.ylabel(ls_names[3])
plt.savefig('scatterLafargevVinci.pdf', format='pdf')

plt.clf()
plt.scatter(ls_rets[:200, 0], ls_rets[:200, 2], c='blue')
plt.xlabel(ls_names[0])
plt.ylabel(ls_names[2])
plt.savefig('scatterAirbusvSG.pdf', format='pdf')
'''