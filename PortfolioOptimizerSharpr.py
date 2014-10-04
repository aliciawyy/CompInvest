'''
This file will store the function which can optimize a portfolio
based on a selection of equities and their result for a chosen 
period

@author: Alicia Wang
@date: 4 Oct 2014
'''
import QSTK.qstkutil.tsutil as tsu
import numpy as np
import matplotlib.pyplot as plt
import pandas.io.data as web
#-------------------------------------------------------------------
def PortfolioOptimizer(startdate, enddate, ls_symbols, ref_symbol,
                       filename = "portfoliovCAC40.pdf"):
    '''
    @param ls_symbols candidates equities
    @parem ref_symbol reference
    
    @return alloc allocation of equities
    '''
    
    # Get the portfolio and reference data from yahoo    
    ldf_data = web.DataReader(ls_symbols, 'yahoo', 
                              start=startdate, end=enddate)   
    ref_data = web.DataReader(ref_symbol, 'yahoo',
                              start=startdate, end=enddate)  
    
    # Clean the NaN of the data
    key_source = 'Adj Close'
    for skey in ['Volume', key_source]:
        '''First forward fill then backward fill'''
        ldf_data[skey] = ldf_data[skey].fillna(method='ffill')
        ldf_data[skey] = ldf_data[skey].fillna(method='bfill')
        ldf_data[skey] = ldf_data[skey].fillna(1.0)
        
        ref_data[skey] = ref_data[skey].fillna(method='ffill')
        ref_data[skey] = ref_data[skey].fillna(method='bfill')
        ref_data[skey] = ref_data[skey].fillna(1.0)       
    
    # Get the adjusted close price and the index of the data
    ls_price  = ldf_data[key_source].values
    ls_date   = ldf_data[key_source].index    
    
    # Get the reference price
    ref_price = ref_data[key_source].values
    ref_date  = ref_data[key_source].index
    
    # Normalizing the prices of the equity candidates and reference
    ls_normalized_price  = ls_price  /  ls_price[0, :]
    ref_normalized_price = ref_price / ref_price[0]


    ndays = 252 # number of trading days per year
    sqrtndays = np.sqrt(ndays)
    
    # Find the portfolio with the highest sharpe ratio
    alloc = range(4)
    
    sharpe_max = 0
    alloc_max  = alloc[:]   
    
    # Temporary solution, only 4 candidates are possible
    for i in range(11):
        alloc[0] = i*0.1
        for j in range (11-i):
            alloc[1] = j*0.1
            for k in range (11-i-j):
                alloc[2] = k*0.1
                alloc[3] = (10-i-j-k)*0.1
                               
                ls_port = np.sum(ls_normalized_price * alloc, axis = 1)  
                ls_portrets = ls_port.copy()
                tsu.returnize0(ls_portrets)   
                
                vol       = np.std(ls_portrets)
                daily_ret = np.average(ls_portrets)
                sharpe    = daily_ret / vol * sqrtndays              
                
                if ( sharpe > sharpe_max ):
                    sharpe_max = sharpe
                    alloc_max  = alloc[:]
                    
    print 'Best sharpe ratio is ', sharpe_max
    print '--------------'  
    print 'Start date:', startdate
    print 'End date:', enddate
    print 'Symbols:', ls_symbols
    print 'Optimal Allocations:', alloc_max 
    
    ls_port = np.sum(ls_normalized_price * alloc, axis = 1)  
    ls_portrets = ls_port.copy()
    tsu.returnize0(ls_portrets)   
    
    vol       = np.std(ls_portrets)
    daily_ret = np.average(ls_portrets)   
    
    print 'Volatility (stdev of daily returns):', vol
    print 'Average daily return:', daily_ret  
    print 'Cumulative return:', ls_port[-1]/ls_port[0]    
    
    # Plotting the prices with x-axis=timestamps
    plt.clf()
    plt.plot(ls_date, ls_port)
    plt.plot(ref_date, ref_normalized_price)
    plt.legend(['Portfolio', ref_symbol])
    plt.ylabel('Normalized Close Price')
    plt.xlabel('Date')
    plt.savefig(filename, format='pdf') 
    
    return alloc_max
    
    