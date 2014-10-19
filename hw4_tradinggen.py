'''
This is a learning version of the homework IV - The trading generator
@author Alicia Wang
@date 19 oct 2014
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import numpy as np
import copy

from GetDataLocal import GetDataLocalYahoo

## ------------------------------------------------------------
def AddOrder(df, date, symbol, transaction, number):
    dic = { df.columns[0]: date.year,
            df.columns[1]: date.month,
            df.columns[2]: date.day,
            df.columns[3]: symbol,
            df.columns[4]: transaction,
            df.columns[5]: number }
    df = df.append(dic, ignore_index = True)
    return df
    
## ------------------------------------------------------------
def GenerateTradingbyEvents(ls_symbols, d_data):
    df_close = d_data['actual_close']
    
    df_event_trading = DataFrame(columns = ["year", "month", "day", 
                                            "symbol", "transaction", "number"])
    
    print "Finding Events"

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)-5):
            
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            
            if f_symprice_yest >= 10.0 and f_symprice_today < 10.0:
                df_event_trading = AddOrder(df_event_trading, ldt_timestamps[i], s_sym, "BUY", 100)
                df_event_trading = AddOrder(df_event_trading, ldt_timestamps[i+5], s_sym, "SELL", 100)
                
    return df_event_trading
## ------------------------------------------------------------
def main():
    '''Main Function'''
    
    dataobj = da.DataAccess('Yahoo')
    
    # Get the symbol list
    ls_symbols = dataobj.get_symbols_from_list("sp5002012")
    ls_symbols.append('SPY') 
    
    # Set the start and end dates of the analysis
    startd = dt.datetime(2008, 1,  1 )
    endd   = dt.datetime(2009, 12, 31)   

    # Get the data from the source of Yahoo (Local store in this example)
    d_data = GetDataLocalYahoo(startd, endd, ls_symbols)
    
    df_event_trading = GenerateTradingbyEvents(ls_symbols, d_data)
    
    df_event_trading.to_csv("orders10d.csv", index = False, header = False)
    
    
## ------------------------------------------------------------
if __name__ == '__main__':
    main()