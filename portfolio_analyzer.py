"""
This is the code of homework 1 to learn QSTK

@author: Alicia Wang
@date: 4 Oct 2014
"""
# QSTK Imports
import QSTK.qstkutil.tsutil as tsu
# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from load_data import load_stock_close_price


def get_portfolio_normalized_price(individual_stock_prices, ls_allocation):
    """
    @param individual_stock_prices: list of individual stock prices
    @param ls_allocation: allocation
    @return: portfolio's normalized price
    """
    normalized_prices = individual_stock_prices / individual_stock_prices[0, :]
    portfolio_normalized_price = np.sum(normalized_prices * ls_allocation, axis=1)
    return portfolio_normalized_price


def analyze(start_date, end_date, ls_symbols, ls_allocation, source='yahoo', debug = False):
    """
    This function analyze the portfolio behavior between the
    startdate and the enddate, it takes four params as following

    @param start_date
    @param end_date
    @param ls_symbols Symbols for for equities
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
    if debug:
        print 'Start date:', start_date
        print 'End date:', end_date
        print 'Symbols:', ls_symbols
        print 'Allocations:', ls_allocation

    stock_close_prices = load_stock_close_price(start_date, end_date, ls_symbols, source)

    ls_port = get_portfolio_normalized_price(stock_close_prices.values, ls_allocation)
    ls_portrets = ls_port.copy()
    daily_return = tsu.returnize0(ls_portrets)

    volatility = np.std(daily_return)
    average_daily_ret = np.average(daily_return)

    # 252 trading days per year
    ndays = 252
    sharpe = average_daily_ret / volatility * np.sqrt(ndays)
    cum_ret = ls_port[-1] / ls_port[0]

    if debug:
        print 'Sharpe Ratio:', sharpe
        print 'Volatility (stdev of daily returns):', volatility
        print 'Average daily return:', average_daily_ret
        print 'Cumulative return:', cum_ret

    return [volatility, average_daily_ret, sharpe, cum_ret]


def plot_portfolio_vs_referance(start_date, end_date, ls_symbols, ls_allocation, ref_symbol):
    """
    This function draws the portfolio in comparison with
    the reference
    """

    stock_close_prices = load_stock_close_price(start_date, end_date, ls_symbols)
    ref_close_price = load_stock_close_price(start_date, end_date, [ref_symbol])

    ls_port = get_portfolio_normalized_price(stock_close_prices.values, ls_allocation)
    ref_normalized_price = get_portfolio_normalized_price(ref_close_price.values, [1])

    # Plot the prices with x-axis=timestamps
    plt.clf()
    plt.plot(stock_close_prices.index, ls_port)
    plt.plot(stock_close_prices.index, ref_normalized_price)
    plt.legend(['Portfolio', ref_symbol])
    plt.ylabel('Normalized Close Price')
    plt.xlabel('Date')
    plt.show()
    # plt.savefig('normalizedPortfoliovReference.pdf', format='pdf')


def test_valid_run():
    vol, ave_daily_ret, sharpe, cum_ret = \
    analyze(dt.datetime(2014, 1, 1), dt.datetime(2014, 12, 31),
            ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2], debug=True)
    eps = 0.1
    assert abs(vol - 0.0072) * 100 < eps
    assert abs(sharpe - 1.24026) * 100 < eps
    assert abs(ave_daily_ret - 0.000567856) * 10000 < eps
    assert abs(cum_ret - 1.146150) * 10000 < eps


def test_draw_portfolio_ref_compare():
    symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
    ref_symbol = '^GSPC'
    plot_portfolio_vs_referance(dt.datetime(2014, 1, 1), dt.datetime(2014, 12, 31),
                                symbols, [0.4, 0.4, 0.0, 0.2], ref_symbol)


def test_best_allocation():
    """
    Test that it is possible to find the best portofolio (highest sharpe ratio)
    given a list of symbols using the methods above.
    """

    # symbols = ['BRCM', 'TXN', 'IBM', 'HNZ'] 
    symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
    # ['GOOG','AAPL','GLD','XOM']
    startd = dt.datetime(2014, 1, 1)
    endd = dt.datetime(2014, 12, 31)

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
                    analyze(startd, endd, symbols, alloc)

                if (sharpe > sharpe_max):
                    sharpe_max = sharpe
                    alloc_max = alloc[:]

    print 'Best sharpe ratio is ', sharpe_max
    print 'Best allocation is', alloc_max

    ref_symbol = '$SPX'

    plot_portfolio_vs_referance(startd, endd, symbols, alloc_max, ref_symbol)


if __name__ == '__main__':
    test_valid_run()
    test_draw_portfolio_ref_compare()
