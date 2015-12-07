"""
This is a market simulation tool which takes an input .csv file for the orders
and gives an .csv value as output.

This program will be launched as following

 $ python hw3_marketsim.py 1000000 orders.csv values.csv

Where the number represents starting cash and orders.csv is a file of orders.


@author Alicia Wang
@date 15 oct 2014
"""

# Third Party Imports
import copy
import csv
import datetime as dt
import numpy as np
import sys

from pandas import Series, DataFrame

from load.load_local_data import load_local_data_from_yahoo


def ReadOrders(filename):
    reader = csv.reader(open(filename, 'rU'), delimiter = ',')
    
    ls_date = []
    ls_symbol = []
    ls_order  = []
    for row in reader:
        ls_date.append(dt.datetime(int(float(row[0])), 
                                   int(float(row[1])), 
                                   int(float(row[2])), 16))
        ls_symbol.append(row[3])
        if row[4] == 'Sell' or row[4] == 'SELL':
            ls_order.append(-int(float(row[5])))
        else:
            ls_order.append(int(float(row[5])))
                
        
    # Create the data
    order_data = { 'date'       :ls_date,
                   'symbol'     :ls_symbol,
                   'transaction':ls_order     }
    
    order_frame = DataFrame(order_data)

    unique_dates   = list(set(ls_date))
    unique_symbols = list(set(ls_symbol))
    
    unique_dates.sort()
      
    return unique_dates, unique_symbols, order_frame
        
#-------------------------------------------------------------------------
def WriteOrders(data_frame, filename):        
    data_frame.to_csv(filename, index = True, header = True)
#-------------------------------------------------------------------------

def main(argv):
    '''Main function'''
    starting_cash = sys.argv[1]
    
    input_file  = sys.argv[2]
    output_file = sys.argv[3]
    
    # Read the order file
    unique_dates, unique_symbols, order_frame = ReadOrders(input_file)
    
    startdate = unique_dates[0]
    enddate   = unique_dates[-1] + dt.timedelta(days = 1)
    price_matrix = load_local_data_from_yahoo(startdate, enddate, unique_symbols)
    
    # Get the price data of the symbols
    price_frame = DataFrame(price_matrix['close'], columns = unique_symbols)
    
    trade_frame = copy.deepcopy(price_frame)
    trade_frame = trade_frame * 0
    
    for i in order_frame.index:
        date     = order_frame.date.ix[i]
        symbol   = order_frame.symbol.ix[i]
        transact = order_frame.transaction.ix[i]
        trade_frame[symbol].ix[date] += transact
        
    nsize = len(trade_frame.index)
    
    cashflow = Series(np.zeros(nsize), index = trade_frame.index)
    
    cashflow[0] = starting_cash


    cashflow -= np.sum(trade_frame * price_frame, axis = 1)

    price_frame['_cash'] = 1.0
    trade_frame['_cash'] = cashflow
    
    hold_frame = np.cumsum(trade_frame, axis = 0)
    
#    print hold_frame

    portfolio = np.sum(hold_frame * price_frame, axis = 1)
    
#    print portfolio

    portfolio.index.name = 'date'
    portfolio.name = 'value'
    WriteOrders(portfolio, output_file)
    
    
#-------------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv[1:])