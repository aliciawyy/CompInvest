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

def simulate(startdate, enddate, ls_symbols, ls_allocation):
    '''
    This function simulate the portfolio behavior between the
    startdate and the enddate, it takes four params as following
    
    @param startdate
    @param enddate
    @param ls_symbols Symbols for for equities (e.g., ['GOOG','AAPL','GLD','XOM'])
    @ls_allocation Allocations to the equities at the beginning of the simulation (e.g., [0.2, 0.3, 0.4, 0.1])
    
    and returns four parameters
    
    @return vol Standard deviation of daily returns of the total portfolio
    @return daily_ret Average daily return of the total portfolio
    @return sharpe Sharpe ratio (Always assume you have 252 trading days 
    in an year. And risk free rate = 0) of the total portfolio
    @return cum_ret Cumulative return of the total portfolio
    ''' 
    
    # Get the data
    ldf_data = web.get_data_yahoo(ls_symbols,start = startdate, end = enddate)
    
    # Clean the NaN of the data
    for skey in ['Adj Close']:
        '''First forward fill then backward fill'''
        ldf_data[skey] = ldf_data[skey].fillna(method='ffill')
        ldf_data[skey] = ldf_data[skey].fillna(method='bfill')
        ldf_data[skey] = ldf_data[skey].fillna(1.0)
    
    # Get the adjusted close price and the index of the data
    ls_price  = ldf_data['Adj Close'].values
    ls_date   = ldf_data['Adj Close'].index    
    
    # Get the daily returns
    ls_rets = ls_price.copy()
    tsu.returnize0(ls_rets)
    
    # Estimate portfolio daily returns
    ls_portrets = np.sum(ls_rets * ls_allocation, axis = 1)
    
    vol = np.std(ls_portrets)
    
    return [vol, daily_ret, sharpe, cum_ret]

def main():
    ''' Main Function'''
    
    startd = dt.datetime(2011, 1, 1)
    endd   = dt.datetime(2011, 12, 31)
    
    symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    allocation = [0.4, 0.4, 0.0, 0.2]
    
    vol, daily_ret, sharpe, cum_ret = simulate(startd, endd, 
                                               symbols, allocation)
    
if __name__ == '__main__':
    main()