"""
Event study of the bollinger band

@author Alicia Wang
@date 5 novembre 2014
"""

# QSTK Imports
import QSTK.qstkstudy.EventProfiler as ep
import QSTK.qstkutil.DataAccess as da
# Third Party Imports
import datetime as dt
import numpy as np
import copy
# Internal Imports
from load.load_local_data import load_local_data_from_yahoo
from hw5_bollingerbands import ComputeBollingerBands
from hw4_tradinggen import GenerateTradingWithEvents


def BollingerEventTest(startd, endd, ls_symbols, lookbackdates):
    
    bolval = ComputeBollingerBands(ls_symbols, startd, endd, lookbackdates)
    ts_market = bolval['SPY']
    
    # Time stamps for the event range
    ldt_timestamps = bolval.index    
    
    df_events = copy.deepcopy(bolval)
    df_events = df_events * np.NAN   
    
    ref = -2.0
    market_ref =  1.4
    
    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            if bolval[s_sym][ldt_timestamps[i-1]]   >= ref \
               and bolval[s_sym][ldt_timestamps[i]] < ref \
               and ts_market[ldt_timestamps[i]] >= market_ref:
                df_events[s_sym][ldt_timestamps[i]] = 1

    return df_events


def main():
    '''main function'''
    
    # Construct the two symbol lists SP 500 of 2008 and 2012
    dataobj = da.DataAccess('Yahoo')    
    
    symbols12 = dataobj.get_symbols_from_list("sp5002012")
    symbols12.append('SPY') 
    
    # Set the start and end dates of the analysis
    startd = dt.datetime(2008, 1,  1 )
    endd   = dt.datetime(2009, 12, 31)  
    
    lookbackdates = 20
    
    
    print 'Start Looking for the events'
    df_events = BollingerEventTest(startd, endd, symbols12, lookbackdates)
    
    print 'Start retrieving data from local Yahoo'
    d_data = load_local_data_from_yahoo(startd, endd, symbols12)
    
    filename = "BollingerEventStudy12.9.pdf"
    
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename = filename, b_market_neutral=True, 
                    b_errorbars = True, s_market_sym='SPY')    

    print 'Generate orders with the events'
    df_event_trading = GenerateTradingWithEvents(df_events)
    df_event_trading.to_csv("ordersbollinger5d.csv", index = False, header = False)


if __name__ == '__main__':
    main()