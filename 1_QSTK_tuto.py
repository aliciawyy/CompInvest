'''
This is the code to learn QSTK

@author: Alicia Wang
@date: 3 Oct 2014
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas.io.data

print "Pandas Version", pd.__version__

#def main():
''' Main Function'''

# List of symbols
ls_symbols = ["AIR.PA", "LG.PA",   "ML.PA",    "DG.PA", "^FCHI" ]  
ls_names   = ["Airbus", "Lafarge", "Michelin", "Vinci", "CAC 40"]

# Start and End date of the charts
dt_start = dt.datetime(2006, 1, 1)
dt_end   = dt.datetime(2014, 10,3)  

ldf_data = pd.io.data.get_data_yahoo(ls_symbols,start=dt_start, end=dt_end)

ls_volume = ldf_data['Volume'].values
ls_price  = ldf_data['Adj Close'].values

ls_date   = ldf_data['Adj Close'].index

plt.plot(ls_date, ls_price)
plt.legend(ls_names)
plt.ylabel('Adjusted Close')
plt.xlabel('Date')
plt.savefig('adjustedclose.pdf', format='pdf')

