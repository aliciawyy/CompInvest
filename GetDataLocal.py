'''
This is to get the data locally
@author Alicia Wang
@date 5 oct 2014
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


##-------------------------------------------------------
def GetDataLocalYahoo(startdate, enddate, ls_symbols):
    
    '''Get the data from local QSTK directory'''
    
    ldt_timestamps = du.getNYSEdays(startdate, enddate, 
                                    dt.timedelta(hours=16))
    
    # Define the keys
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']    
    
    dataobj = da.DataAccess('Yahoo')
    
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    
    # Range the data
    d_data = dict(zip(ls_keys, ldf_data)) 
    
    # Clean the data
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0) 
        
    # return a dict object of data well cleaned
    return d_data

#--------------------------------------------------------------
def GetDataLocalYahoo_dates(ldt_timestamps, ls_symbols):
    
    '''Get the data from local QSTK directory'''
    
    # Define the keys
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']    
    
    dataobj = da.DataAccess('Yahoo')
    
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    
    # Range the data
    d_data = dict(zip(ls_keys, ldf_data)) 
    
    # Clean the data
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0) 
        
    # return a dict object of data well cleaned
    return d_data