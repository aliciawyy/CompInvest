"""
This file contains the function to compute the bollinger bands
for a certain symbole.

@author Alicia Wang
@date 30 oct 2014
"""
import datetime as dt
import matplotlib.pyplot as plt
import pandas.stats.moments as ts
from pandas import DataFrame

# Internal Import
from portfolio import BasicPortfolio


def compute_bollinger_band(basic_portfolio, period, source='yahoo',
                           filename=None):
    """
    Compute the bollinger band for a list of stocks.
    @param basic_portfolio: A basic portfolio instance
    @param period:
    @param source: source to get the data
    @param filename:
    @return:
    """

    assert isinstance(basic_portfolio, BasicPortfolio)
    stock_close_prices = basic_portfolio.get_stock_close_prices(source)
    
    basic_portfolio.print_information()
    print 'Lookback period : ', period
        
    bol_mean = ts.rolling_mean(stock_close_prices, period)
    bol_std = ts.rolling_std(stock_close_prices, period)
    
    bollinger_band_up = bol_mean + bol_std
    bollinger_band_down = bol_mean - bol_std

    plt.clf()
    plt.plot(stock_close_prices.index, stock_close_prices.values)
    plt.plot(stock_close_prices.index, bollinger_band_up)
    plt.plot(stock_close_prices.index, bollinger_band_down)
    plt.legend(['Stock adjusted price', 'Bollinger band', 'Bollinger band'])
    plt.ylabel('Price')
    plt.xlabel('Date')
    if filename is not None:
        plt.savefig(filename, format='pdf')
    else:
        plt.show()
    
    bol_val = (stock_close_prices - bol_mean)/bol_std
    val = DataFrame(bol_val, index=stock_close_prices.index,
                    columns=basic_portfolio.tickers)
    
    # print val[-5:]
    val.to_csv('result/bol.csv')
    
    # return the bollinger value
    return val
    

def test():
    """Main Function"""
    ls_symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
    start_date = dt.datetime(2010, 1,  1)
    end_date = dt.datetime(2010, 12, 31)
    basic_portfolio = BasicPortfolio(ls_symbols, start_date, end_date)
    period = 20
    
    compute_bollinger_band(basic_portfolio, period, source='local')


if __name__ == '__main__':
    test()
