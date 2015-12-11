"""
This file regroups some basic analysis functions
of portfolio.

@author: Alice Wang
"""
import QSTK.qstkutil.tsutil as tsu
import datetime as dt
import numpy as np
from portfolio import BasicPortfolio


def get_daily_return0(stock_normalized_prices):
    tmp = stock_normalized_prices.copy()
    return tsu.returnize0(tmp)


def analyze(basic_portfolio, ls_allocation, source='yahoo', debug=False):
    """
    This function analyze the portfolio behavior between the
    start_date and the end_ate, it takes four params as following

    @param basic_portfolio
    (e.g., ['GOOG','AAPL','GLD','XOM'])
    @param ls_allocation Allocations to the equities at the beginning of the
    simulation (e.g., [0.2, 0.3, 0.4, 0.1])
    @param source to get the data ('yahoo', 'google', 'local')

    and returns four parameters

    @return volatility Standard deviation of daily returns of the total portfolio
    @return average_daily_ret Average daily return of the total portfolio
    @return sharpe Sharpe ratio (Always assume you have 252 trading days
    in an year. And risk free rate = 0) of the total portfolio
    @return cum_ret Cumulative return of the total portfolio
    """
    assert isinstance(basic_portfolio, BasicPortfolio)
    if debug:
        basic_portfolio.print_information()
        print 'Allocations:', ls_allocation

    portfolio_price = basic_portfolio.get_portfolio_normalized_price(ls_allocation, source)
    daily_return = get_daily_return0(portfolio_price)

    volatility = np.std(daily_return)
    average_daily_ret = np.average(daily_return)

    # 252 trading days per year
    ndays = 252
    sharpe = average_daily_ret / volatility * np.sqrt(ndays)
    cum_ret = portfolio_price[-1] / portfolio_price[0]

    if debug:
        print 'Sharpe Ratio:', sharpe
        print 'Volatility (stdev of daily returns):', volatility
        print 'Average daily return:', average_daily_ret
        print 'Cumulative return:', cum_ret

    return [volatility, average_daily_ret, sharpe, cum_ret]


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
                    analyze(basic_portfolio, alloc)

                if sharpe > sharpe_max:
                    sharpe_max = sharpe
                    alloc_max = alloc[:]

    print 'Best sharpe ratio is ', sharpe_max
    print 'Best allocation is', alloc_max

    ref_symbol = '$SPX'

    basic_portfolio.plot_with_reference(alloc_max, ref_symbol, source='local')


if __name__ == '__main__':
    test_draw_portfolio_ref_compare()
