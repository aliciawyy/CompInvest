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
import copy

from GetDataLocal import GetDataLocalYahoo

## ------------------------------------------------------------
def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    
    df_close = d_data['actual_close']

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
            
            if f_symprice_yest >= 9.0 and f_symprice_today < 9.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events    

## ------------------------------------------------------------
def EventTest(startd, endd, ls_symbols, filename = "MyEventStudy.pdf"):
    
    d_data = GetDataLocalYahoo(startd, endd, ls_symbols)
    
    df_events = find_events(ls_symbols, d_data)
    
    print 'Number of events', np.sum(np.sum(df_events.notnull()))
        
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename = filename, b_market_neutral=True, 
                b_errorbars = True, s_market_sym='SPY')    


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
  
    EventTest(startd, endd, symbols08, "MyEventStudy08.9.pdf")
    EventTest(startd, endd, symbols12, "MyEventStudy12.9.pdf")
       
    
## ------------------------------------------------------------
if __name__ == '__main__':
    main()