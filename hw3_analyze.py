'''
This file contains the function to compare the performance of a portfolio with
a reference. It will be called like

 $ python hw3_analyze.py values.csv \$SPX
 
@author Alicia Wang
@date 15 oct 2014
'''

from pandas import Series, DataFrame
from GetDataLocal import GetDataLocalYahoo

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.parser import parse

import QSTK.qstkutil.tsutil as tsu


## ------------------------------------------------------------
def Analyze(input_file, ref_symbol):
    
    # Load the portfolio value from the input file
    portfolio = pd.read_csv(input_file, index_col = 'date')
    
    print 'Details of the Performance of the portfolio with the reference ',
    print ref_symbol
    print ' '
    
    print 'Data Range : ', portfolio.index[0],
    print ' to ', portfolio.index[-1]
    print ' '
    
    dates = []
    for i in range(len(portfolio.index)):
        dates.append(parse(portfolio.index[i]))
        
    # Load the value of the reference data
    ref_data = GetDataLocalYahoo(dates[0], 
                                 dates[-1],
                                 [ref_symbol])    

    # Normalizing the prices   
    port_norm = portfolio.values[:]/portfolio.values[0]
    ref_norm  = ref_data['close'].values[:]/ref_data['close'].values[0]
   
    # Plotting the prices with x-axis=timestamps
    plt.clf()
    plt.plot(dates, port_norm)
    plt.plot(dates, ref_norm)
    plt.legend(['Portfolio', ref_symbol])
    plt.ylabel('Normalized Close Price')
    plt.xlabel('Date')
    plt.savefig('marketsimPortvReference.pdf', format='pdf') 
    
    '''
    Expected result for order-short.csv
    Sharpe Ratio of Fund : -0.449182051041
    Sharpe Ratio of $SPX : 0.88647463107
    
    Total Return of Fund :  0.998035
    Total Return of $SPX : 1.00289841449
    
    Standard Deviation of Fund :  0.00573613516299
    Standard Deviation of $SPX : 0.00492987789459
    
    Average Daily Return of Fund :  -0.000162308588036
    Average Daily Return of $SPX : 0.000275297459588
    '''
    
    print 'Total Return of Fund : ', (port_norm[-1]/port_norm[0])[0]
    print 'Total Return of ', ref_symbol, ' : ', (ref_norm[-1]/ref_norm[0])[0]
    print ' '
    
    ndays = 252 # number of trading days in a year

    portret = port_norm.copy()
    tsu.returnize0(portret)
    daily_ret_port = np.average(portret)
    vol_port = np.std(portret)
    
    refret = ref_norm.copy()
    tsu.returnize0(refret)
    daily_ret_ref = np.average(refret)
    vol_ref = np.std(refret)

    print 'Volatility of Fund : ', vol_port
    print 'Volatility of ', ref_symbol, ' : ', vol_ref
    print ' '
    print 'Average Daily Return of Fund : ', daily_ret_port
    print 'Average Daily Return of ', ref_symbol, ' : ', daily_ret_ref
    print ' '
    
    sharpe_port = daily_ret_port / vol_port * np.sqrt(ndays)
    sharpe_ref  = daily_ret_ref / vol_ref * np.sqrt(ndays)
    
    print 'Sharpe Ratio of Fund : ', sharpe_port
    print 'Sharpe Ratio of ', ref_symbol, ' : ', sharpe_ref

## ------------------------------------------------------------
def main(argv):
    '''Main function'''
        
    # file containing the values of the portfolio
    input_file  = sys.argv[1]
    
    # reference symbol
    ref_symbol  = sys.argv[2]   
    
    Analyze(input_file, ref_symbol)


## ------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv[1:])
    