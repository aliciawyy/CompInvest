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
    
    source = 'local' # 'yahoo', 'google', 'local'
    '''
    # Get the data    
    ldf_data = web.DataReader(ls_symbols, source,
                              start=startdate, end=enddate)
    '''
    if source == 'google': 
        key_source = 'Close'
    elif source == 'yahoo':
        key_source = 'Adj Close'
    elif source == 'local':
        key_source = 'close'    
    
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)
    
    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']    
    
    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data0 = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    ldf_data = dict(zip(ls_keys, ldf_data0))    
    
    # Clean the NaN of the data
    for skey in [key_source]:
        '''First forward fill then backward fill'''
        ldf_data[skey] = ldf_data[skey].fillna(method='ffill')
        ldf_data[skey] = ldf_data[skey].fillna(method='bfill')
        ldf_data[skey] = ldf_data[skey].fillna(1.0)
    
    # Get the adjusted close price and the index of the data
    ls_price  = ldf_data[key_source].values
    ls_date   = ldf_data[key_source].index    
    
    # Normalizing the prices
    ls_normalized_price = ls_price / ls_price[0, :]
      
    # 252 trading days per year
    ndays = 252
    
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

def draw_compare(startdate, enddate, ls_symbols, ls_allocation, ref_symbol):
    '''
    This function draws the portfolio in comparison with 
    the reference
    '''
    
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)
    
    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']    
    
    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data0 = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    ldf_data  = dict(zip(ls_keys, ldf_data0))    
    
    ref_data0  = c_dataobj.get_data(ldt_timestamps, [ref_symbol], ls_keys)
    ref_data  = dict(zip(ls_keys, ref_data0)) 
    
    # Clean the NaN of the data
    for skey in ls_keys:
        '''First forward fill then backward fill'''
        ldf_data[skey] = ldf_data[skey].fillna(method='ffill')
        ldf_data[skey] = ldf_data[skey].fillna(method='bfill')
        ldf_data[skey] = ldf_data[skey].fillna(1.0)
        
        ref_data[skey] = ref_data[skey].fillna(method='ffill')
        ref_data[skey] = ref_data[skey].fillna(method='bfill')
        ref_data[skey] = ref_data[skey].fillna(1.0)
    
    key_source = 'close'
    
    # Get the adjusted close price and the index of the data
    ls_price  = ldf_data[key_source].values    
    ref_price = ref_data[key_source].values
    
    # Normalizing the prices
    ls_normalized_price  = ls_price  /  ls_price[0, :]
    ref_normalized_price = ref_price / ref_price[0, :]
    
    # Estimate portfolio daily returns
    ls_port     = np.sum(ls_normalized_price * ls_allocation, axis = 1)
    
    # Plotting the prices with x-axis=timestamps
    plt.clf()
    plt.plot(ldt_timestamps, ls_port)
    plt.plot(ldt_timestamps, ref_normalized_price)
    plt.legend(['Portfolio', ref_symbol])
    plt.ylabel('Normalized Close Price')
    plt.xlabel('Date')
    plt.savefig('normalizedPortfoliovReference.pdf', format='pdf')    
             
def main():
    ''' Main Function'''

    print '==== Test 1 ===='
    vol, daily_ret, sharpe, cum_ret = \
        simulate(dt.datetime(2011, 1, 1), dt.datetime(2011, 12, 31), 
                 ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2], 
                 print_opt = True)
    
    print '==== Test 2 ===='
    vol, daily_ret, sharpe, cum_ret = \
        simulate(dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31), 
                 ['AXP', 'HPQ', 'IBM', 'HNZ'], [0.0, 0.0, 0.0, 1.0],
                 print_opt = True)   
    
    print '================================='
    print 'Next, we will find the best allocation of the portfolio'
    print 'which could have the highest sharpe ratio'
    
    # symbols = ['BRCM', 'TXN', 'IBM', 'HNZ'] 
    symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']  
    # ['GOOG','AAPL','GLD','XOM']
    startd  = dt.datetime(2011, 1, 1)
    endd    = dt.datetime(2011, 12, 31)
    
    alloc = range(4)
    
    sharpe_max = 0
    alloc_max  = alloc[:]
    
    for i in range(11):
        alloc[0] = i*0.1
        for j in range (11-i):
            alloc[1] = j*0.1
            for k in range (11-i-j):
                alloc[2] = k*0.1
                alloc[3] = (10-i-j-k)*0.1
                               
                vol, daily_ret, sharpe, cum_ret = \
                simulate(startd, endd, symbols, alloc)      
                
                if ( sharpe > sharpe_max ):
                    sharpe_max = sharpe
                    alloc_max  = alloc[:]
                    
    print 'Best sharpe ratio is ', sharpe_max
    print 'Best allocation is', alloc_max
    
    ref_symbol = '$SPX'
    
    draw_compare(startd, endd, symbols, alloc_max, ref_symbol)
    
if __name__ == '__main__':
    main()