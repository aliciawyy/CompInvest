'''
This file will store the function which will determine
the efficient frontier

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

#-----------------------------------------------------------------------
def getFrontier(startdate, enddate, ls_symbols, ref_symbol,
                ls_names = [], filename = "EquitiesvFrontier.pdf"):
    '''
    @param ls_symbols candidates equities
    @param ls_names   candidates names
    @parem ref_symbol reference
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
    
    
    ## Optimize the efficient frontier
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
        
    f_target = 0.0015
    (na_weights, f_std, b_error) = \
                tsu.OptPort(na_data, f_target, na_lower, na_upper, s_type="long")
    
    print 'Optimized portfolio for target return', f_target
    print 'Volatility is ', f_std

    for i in range(len(na_weights)):
        if na_weights[i] > 0.00001:
            print ls_names[i], ':', na_weights[i]
        
        
        
    plt.clf()
    
    fig = plt.figure(figsize=(8, 10), dpi=100)
    
    # Plot indivisual stock risk/return as green +
    for i in range(len(ls_symbols)):
#        plt.plot(na_std[i], f_ret, 'g+') 
#        plt.text(na_std[i], f_ret, ls_names[i], fontsize = 10)
        ave = np.average(na_data[:,i])
        std = np.std(na_data[:,i])
        plt.plot(std, ave, 'g+') 
        plt.text(std, ave, ls_names[i], fontsize = 5)   
        
    ref_data = ref_normalized_price.copy()
    tsu.returnize0(ref_data) 
    ave = np.average(ref_data)
    std = np.std(ref_data)    
    plt.plot(std, ave, 'r+') 
    plt.text(std, ave, 'CAC 40', fontsize = 6)    
        
    plt.plot(lf_std, lf_returns, 'b') 
        
    plt.title('Efficient Frontier For CAC 40')
#    plt.legend(['2013 Frontier'], loc = 'lower left')
    plt.ylabel('Expected Return')
    plt.xlabel('StDev')
    plt.savefig(filename, format='pdf')
    

#-----------------------------------------------------------
def main():
    symbols     = ['AIR.PA', 'LG.PA', 'GLE.PA', 'DG.PA']
    ref_symbol  = '^FCHI'
    
    endd        = dt.datetime.today()
    startd      = endd - dt.timedelta(days = 365*2)
    
    cac40_orig  = LoadCAC40()
    
    cac40_modif = cac40_orig.drop(['SAN.PA', 'UL.PA'])
    
    getFrontier(startd, endd, cac40_modif.index, ref_symbol,
                ls_names = cac40_modif.values)     

#----------------------------------------------------------
if __name__ == '__main__':
    main()