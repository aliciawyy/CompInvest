"""
This file regroups some basic analysis functions
of portfolio.

@author: Alice Wang
"""
import QSTK.qstkutil.tsutil as tsu
import datetime as dt
import numpy as np
from portfolio import BasicPortfolio


def test_draw_portfolio_ref_compare():
    symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
    ref_symbol = '^GSPC'
    basic_portfolio = BasicPortfolio(symbols, dt.datetime(2014, 1, 1), dt.datetime(2014, 12, 31))
    basic_portfolio.plot_with_reference([0.4, 0.4, 0.0, 0.2], ref_symbol, source='yahoo')


def test_best_allocation():
    """
    This function is to remove
    Test that it is possible to find the best portfolio (highest sharpe ratio)
    given a list of symbols using the methods above.
    """

    # symbols = ['BRCM', 'TXN', 'IBM', 'HNZ'] 
    symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
    # ['GOOG','AAPL','GLD','XOM']
    basic_portfolio = BasicPortfolio(symbols, dt.datetime(2014, 1, 1), dt.datetime(2014, 12, 31))

    alloc = range(4)

    sharpe_max = 0
    alloc_max = alloc[:]

    for i in range(11):
        alloc[0] = i * 0.1
        for j in range(11 - i):
            alloc[1] = j * 0.1
            for k in range(11 - i - j):
                alloc[2] = k * 0.1
                alloc[3] = (10 - i - j - k) * 0.1

                vol, daily_ret, sharpe, cum_ret = \
                    basic_portfolio.analyze(alloc)

                if sharpe > sharpe_max:
                    sharpe_max = sharpe
                    alloc_max = alloc[:]

    print 'Best sharpe ratio is ', sharpe_max
    print 'Best allocation is', alloc_max

    ref_symbol = '$SPX'

    basic_portfolio.plot_with_reference(alloc_max, ref_symbol, source='local')


if __name__ == '__main__':
    test_draw_portfolio_ref_compare()
