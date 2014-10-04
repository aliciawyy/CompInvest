'''
This is the code of homework 1 to learn QSTK

@author: Alicia Wang
@date: 4 Oct 2014
'''
# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas.io.data as web

from PortfolioOptimizerSharpr import PortfolioOptimizer

# Global variables
source = 'yahoo' # 'yahoo', 'google', 'local'

if source == 'google': 
    key_source = 'Close'
elif source == 'yahoo':
    key_source = 'Adj Close'
elif source == 'local':
    key_source = 'close'
    
# 252 trading days per year
ndays = 252

# ----------------------------------------------------------------------------
def simulate(startdate, enddate, ls_symbols, ls_allocation, print_opt = False):
    '''
    This function simulate the portfolio behavior between the
    startdate and the enddate, it takes four params as following
    
    @param startdate
    @param enddate
    @param ls_symbols Symbols for for equities 
    (e.g., ['GOOG','AAPL','GLD','XOM'])
    @ls_allocation Allocations to the equities at the beginning of the 
    simulation (e.g., [0.2, 0.3, 0.4, 0.1])
    
    and returns four parameters
    
    @return vol Standard deviation of daily returns of the total portfolio
    @return daily_ret Average daily return of the total portfolio
    @return sharpe Sharpe ratio (Always assume you have 252 trading days 
    in an year. And risk free rate = 0) of the total portfolio
    @return cum_ret Cumulative return of the total portfolio
    ''' 
    if print_opt:
        print 'Start date:', startdate
        print 'End date:', enddate
        print 'Symbols:', ls_symbols
        print 'Optimal Allocations:', ls_allocation
    
    # Get the data    
    ldf_data = web.DataReader(ls_symbols, source,
                              start=startdate, end=enddate)
    
    # Clean the NaN of the data
    for skey in ['Volume', key_source]:
        '''First forward fill then backward fill'''
        ldf_data[skey] = ldf_data[skey].fillna(method='ffill')
        ldf_data[skey] = ldf_data[skey].fillna(method='bfill')
        ldf_data[skey] = ldf_data[skey].fillna(1.0)
    
    # Get the adjusted close price and the index of the data
    ls_price  = ldf_data[key_source].values
    ls_date   = ldf_data[key_source].index    
    
    # Normalizing the prices
    ls_normalized_price = ls_price / ls_price[0, :]  
    
    # Estimate portfolio daily returns
    ls_port     = np.sum(ls_normalized_price * ls_allocation, axis = 1)
    ls_portrets = ls_port.copy()
    tsu.returnize0(ls_portrets)
    
    vol       = np.std(ls_portrets)
    daily_ret = np.average(ls_portrets)
    sharpe    = daily_ret / vol * np.sqrt(ndays)
    cum_ret   = ls_port[-1]/ls_port[0]
    
    if print_opt:
        print 'Sharpe Ratio:', sharpe
        print 'Volatility (stdev of daily returns):', vol
        print 'Average daily return:', daily_ret  
        print 'Cumulative return:', cum_ret
    
    return [vol, daily_ret, sharpe, cum_ret]    

# -------------------------------------------------------------------            
def main():
    ''' Main Function'''

    symbols = ["AIR.PA", "LG.PA",   "GLE.PA",    "DG.PA"]
    # symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']  
    # ['GOOG','AAPL','GLD','XOM']
    startd  = dt.datetime(2013, 10, 1)
    # endd    = dt.datetime(2013, 12, 31)   
    endd    = dt.datetime.today()
    
    print '==== Test 1 ===='
    vol, daily_ret, sharpe, cum_ret = \
        simulate(dt.datetime(2011, 1, 1), dt.datetime(2011, 12, 31), 
                 symbols, [0.4, 0.4, 0.0, 0.2], print_opt = True)
    
    print '==== Test 2 ===='
    vol, daily_ret, sharpe, cum_ret = \
        simulate(dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31), 
                 ['AXP', 'HPQ', 'IBM', 'HNZ'], [0.0, 0.0, 0.0, 1.0],
                 print_opt = True)   
    
    print '================================='
    print 'Next, we will find the best allocation of the portfolio'
    print 'which could have the highest sharpe ratio'
    
    ref_symbol = '^FCHI' # CAC 40
    
    PortfolioOptimizer(startd, endd, symbols, ref_symbol, filename = "portfoliovCAC40.pdf")
    
if __name__ == '__main__':
    main()
