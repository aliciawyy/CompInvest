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
from bollinger_band import compute_bollinger_band
from hw4_tradinggen import GenerateTradingWithEvents
from portfolio import BasicPortfolio


def BollingerEventTest(basic_portfolio, lookbackdates):
    
    bolval = compute_bollinger_band(basic_portfolio, lookbackdates, 'local')
    ts_market = bolval['SPY']
    
    # Time stamps for the event range
    ldt_timestamps = bolval.index    
    
    df_events = copy.deepcopy(bolval)
    df_events = df_events * np.NAN   
    
    ref = -2.0
    market_ref = 1.4
    
    for s_sym in basic_portfolio.tickers:
        for i in range(1, len(ldt_timestamps)):
            if (bolval[s_sym][ldt_timestamps[i - 1]] >= ref) and (
                        bolval[s_sym][ldt_timestamps[i]] < ref) and (
                        ts_market[ldt_timestamps[i]] >= market_ref):
                df_events[s_sym][ldt_timestamps[i]] = 1

    return df_events


def main():
    """main function"""
    
    # Construct the two symbol lists SP 500 of 2008 and 2012
    dataobj = da.DataAccess('Yahoo')    
    
    symbols12 = dataobj.get_symbols_from_list("sp5002012")
    symbols12.append('SPY')
    
    lookbackdates = 20
    basic_portfolio = BasicPortfolio(symbols12, dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31))
    
    print 'Start Looking for the events'
    df_events = BollingerEventTest(basic_portfolio, lookbackdates)
    
    print 'Start retrieving data from local Yahoo'
    d_data = load_local_data_from_yahoo(basic_portfolio.start_date,
                                        basic_portfolio.end_date,
                                        basic_portfolio.tickers)
    
    filename = "BollingerEventStudy12.9.pdf"
    
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename = filename, b_market_neutral=True, 
                    b_errorbars = True, s_market_sym='SPY')    

    print 'Generate orders with the events'
    df_event_trading = GenerateTradingWithEvents(df_events)
    df_event_trading.to_csv("ordersbollinger5d.csv", index = False, header = False)


if __name__ == '__main__':
    main()
