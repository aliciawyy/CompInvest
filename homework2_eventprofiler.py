'''
This is a learning version of the homework II - The Event Profiler
@author Alicia Wang
@date 5 oct 2014
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from GetDataLocal import GetDataLocalYahoo

## ------------------------------------------------------------
def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    
    df_close = d_data['close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol is down more then 3% while the
            # market is up more then 2%
            if f_symprice_yesty >= 5.0 and f_symprice_today < 5.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events    

## ------------------------------------------------------------
def main():
    '''Main Function'''
    
    # Construct the two symbol lists SP 500 of 2008 and 2012
    dataobj = da.DataAccess('Yahoo')
    symbols08 = dataobj.get_symbols_from_list("sp5002008")
    symbols08.append('SPY')  
    
    symbols12 = dataobj.get_symbols_from_list("sp5002012")
    symbols12.append('SPY') 
    
    # Set the start and end dates of the analysis
    startd = dt.datetime(2008, 1,  1 )
    endd   = dt.datetime(2009, 12, 31)    
  
    # Get the data of the two lists for the same period
    d_data08 = GetDataLocalYahoo(startd, endd, symbols08)
    d_data12 = GetDataLocalYahoo(startd, endd, symbols12)
    
    df_events08 = find_events(symbols08, d_data08)
    df_events12 = find_events(symbols12, d_data12)
    
    print "Creating Study 2008"
    ep.eventprofiler(df_events08, d_data08, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy08.pdf', b_market_neutral=True, 
                b_errorbars=True, s_market_sym='SPY')
    
    print "Creating Study 2012"
    ep.eventprofiler(df_events12, d_data12, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy12.pdf', b_market_neutral=True, 
                b_errorbars=True, s_market_sym='SPY')    
    

## ------------------------------------------------------------
if __name__ == '__main__':
    main()