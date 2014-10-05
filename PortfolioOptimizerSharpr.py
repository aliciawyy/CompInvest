'''
This file will store the function which can optimize a portfolio
based on a selection of equities and their result for a chosen 
period

@author: Alicia Wang
@date: 4 Oct 2014
'''

# QSTK Imports
import QSTK.qstkutil.tsutil as tsu

# Third Party import
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas.io.data as web

from LoadTicker import LoadCAC40
#-------------------------------------------------------------------
def PortfolioOptimizer(startdate, enddate, ls_symbols, ref_symbol,
                       filename = "portfoliovCAC40.pdf", ls_names = []):
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

    na_data = ls_normalized_price.copy()
    tsu.returnize0(na_data)
    
    # Special Case with fTarget=None, just returns average rets.
    (na_avgrets, na_std, b_error) = tsu.OptPort(na_data, None)  
    
    # Declaring bounds on the optimized portfolio
    na_lower = np.zeros(na_data.shape[1])
    na_upper = np.ones(na_data.shape[1])    

    # Getting the range of possible returns with these bounds
    (f_min, f_max) = tsu.getRetRange(na_data, na_lower, na_upper,
                            na_avgrets, s_type="long")

    # Getting the step size and list of returns to optimize for.
    f_step = (f_max - f_min) / 100.0
    lf_returns = [f_min + x * f_step for x in range(101)]
    
    # Declaring empty lists
    lf_std = []
    lna_portfolios = []

    # Calling the optimization for all returns
    for f_target in lf_returns:
        (na_weights, f_std, b_error) = \
            tsu.OptPort(na_data, f_target, na_lower, na_upper, s_type="long")
        lf_std.append(f_std)
        lna_portfolios.append(na_weights)    
        
    plt.clf()
    plt.plot(lf_std, lf_returns, 'b')   
    
    # Plot indivisual stock risk/return as green +
    for i, f_ret in enumerate(na_avgrets):
        plt.plot(na_std[i], f_ret, 'g+') 
        plt.text(na_std[i], f_ret, ls_names[i])
        
    plt.title('Efficient Frontier For CAC 40')
    plt.legend(['2013 Frontier'], loc = 'lower left')
    plt.ylabel('Expected Return')
    plt.xlabel('StDev')
    plt.savefig('Frontier2013.pdf', format='pdf')
    
    '''
    ndays = len(ls_price) # trading days
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
    print 'The sharpe ratio of reference (', ref_symbol, ') is'
    print np.std(ref_normalized_price)/np.average(ref_normalized_price) * sqrtndays
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
    
    print 'Volatility (stdev of daily returns)/reference volatility:', vol, \
          '/', np.std(ref_normalized_price)
    print 'Average daily return', daily_ret
    print 'Cumulative return/reference return:', ls_port[-1]/ls_port[0], \
          '/', ref_normalized_price[-1]/ref_normalized_price[0]
    
   
    # Plotting the prices with x-axis=timestamps
    plt.clf()
    plt.plot(ls_date, ls_port)
    plt.plot(ref_date, ref_normalized_price)
    plt.legend(['Portfolio', ref_symbol])
    plt.ylabel('Normalized Close Price')
    plt.xlabel('Date')
    plt.savefig(filename, format='pdf') 
    
    return alloc_max
    '''
#----------------------------------------    
def main():
    symbols = ["AIR.PA", "LG.PA", "GLE.PA", "DG.PA"]
    ref_symbol = '^FCHI'
    
    endd    = dt.datetime.today()
    startd  = endd - dt.timedelta(days = 365)
    
    cac40_orig = LoadCAC40()
    
    cac40_modif = cac40_orig.drop(['SAN.PA', 'UL.PA'])
    

    # PortfolioOptimizer(startd, endd, symbols, ref_symbol,
    #                      filename = "portfoliovCAC40.pdf")
    
    PortfolioOptimizer(startd, endd, cac40_modif.index, ref_symbol,
                               ls_names = cac40_modif.index)     

#----------------------------------------
if __name__ == '__main__':
    main()