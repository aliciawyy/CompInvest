'''
This file contains the function to compute the bollinger bands
for a certain symbole.

@author Alicia Wang
@date 30 oct 2014
'''
# Third Party Imports
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from pandas import DataFrame, Series
import pandas.stats.moments as ts

# Internal Imports
from GetDataLocal import GetDataLocalYahoo

## ------------------------------------------------------------
def ComputeBollingerBands(ls_symbols, startdate, enddate, period, filename = ''):
    
    # Get the data from local repository
    d_data = GetDataLocalYahoo(startdate, enddate, ls_symbols)
    
    print 'Symbol : ', ls_symbols
    print 'Start date : ', startdate
    print 'Start date : ', enddate
    print 'Lookback period : ', period
    
    df_close = d_data['actual_close']
        
    bol_mean = ts.rolling_mean(df_close, period)
    bol_std = ts.rolling_std(df_close, period)    
    
    bolband_up = bol_mean + bol_std
    bolband_dw = bol_mean - bol_std
        
    # Plotting the prices with x-axis=timestamps
    if filename is not '':
        plt.clf()
        plt.plot(df_close.index, df_close.values)
        plt.plot(df_close.index, bolband_up)
        plt.plot(df_close.index, bolband_dw)
        plt.legend(['Stock adjusted price', 'Bollinger band', 'Bollinger band'])
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.savefig(filename, format='pdf')     
    
    bol_val = (df_close - bol_mean)/bol_std
    val = DataFrame(bol_val, index = df_close.index, 
                    columns = ls_symbols)
    
    print val[-5:]
    val.to_csv('bol.csv')
    
    
    
    
    
## ------------------------------------------------------------
def main():
    '''Main Function'''
    ls_symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
    startd     = dt.datetime(2010, 1,  1)
    endd       = dt.datetime(2010, 12, 31)
    period     = 20
    
    ComputeBollingerBands(ls_symbols, startd, endd, period, 
                          "GoogleBollingerBand.pdf")
    
    
 
## ------------------------------------------------------------
if __name__ == '__main__':
    main()