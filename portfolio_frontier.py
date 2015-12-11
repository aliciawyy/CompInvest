"""
This file will store the function which will determine
the efficient frontier

@author: Alicia Wang
@date: 4 Oct 2014
"""

# QSTK Imports
import QSTK.qstkutil.tsutil as tsu
# Third Party import
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from load.load_ticker import load_valid_cac40_names
from load.load_data import load_stock_close_price
from portfolio_analyzer import get_daily_return0, plot_portfolio_vs_referance
from portfolio import BasicPortfolio


def get_frontier(basic_portfolio, ref_symbol, filename="EquitiesvFrontier.pdf",
                 target_return=0.015):
    """
    @param basic_portfolio
    @param ref_symbol reference symbol
    """

    assert isinstance(basic_portfolio, BasicPortfolio)
    stock_close_price = basic_portfolio.get_stock_close_prices()

    stock_normalized_price = stock_close_price.values / stock_close_price.values[0, :]

    ref_close_price = load_stock_close_price(start_date, end_date, [ref_symbol])
    ref_normalized_price = ref_close_price.values / ref_close_price.values[0, :]

    daily_return0 = get_daily_return0(stock_normalized_price)

    (na_avgrets, na_std, b_error) = tsu.OptPort(daily_return0, None)

    # Declaring bounds on the optimized portfolio
    na_lower = np.zeros(daily_return0.shape[1])
    na_upper = np.ones(daily_return0.shape[1])

    # Getting the range of possible returns with these bounds
    (f_min, f_max) = tsu.getRetRange(daily_return0, na_lower, na_upper,
                                     na_avgrets, s_type="long")

    # Getting the step size and list of returns to optimize for.
    f_step = (f_max - f_min) / 100.0
    lf_returns = [f_min + x * f_step for x in range(101)]

    # Declaring empty lists
    lf_std = []
    lna_portfolios = []

    # Calling the optimization for all returns
    for f_target in lf_returns:
        (na_weights, f_std, b_error) = \
            tsu.OptPort(daily_return0, f_target, na_lower, na_upper, s_type="long")
        lf_std.append(f_std)
        lna_portfolios.append(na_weights)

    f_target = target_return
    (na_weights, f_std, b_error) = \
        tsu.OptPort(daily_return0, f_target, na_lower, na_upper, s_type="long")

    print 'Optimized portfolio for target return', f_target
    print 'Volatility is ', f_std

    for ticker_name, weight in zip(basic_portfolio.ticker_names, na_weights):
        if weight > 0.00001:
            print ticker_name, ':', weight

    plt.clf()
    plt.figure(figsize=(8, 10), dpi=100)

    # Plot individual stock risk/return as green +
    for i in range(len(basic_portfolio.ticker_names)):
        #        plt.plot(na_std[i], f_ret, 'g+')
        #        plt.text(na_std[i], f_ret, ls_names[i], fontsize = 10)
        ave = np.average(daily_return0[:, i])
        std = np.std(daily_return0[:, i])
        plt.plot(std, ave, 'g+')
        plt.text(std, ave, basic_portfolio.ticker_names[i], fontsize=5)

    ref_daily_return = get_daily_return0(ref_normalized_price)
    ave = np.average(ref_daily_return)
    std = np.std(ref_daily_return)
    plt.plot(std, ave, 'r+')
    plt.text(std, ave, 'CAC 40', fontsize=6)

    plt.plot(lf_std, lf_returns, 'b')

    plt.title('Efficient Frontier For CAC 40')
    #    plt.legend(['2013 Frontier'], loc = 'lower left')
    plt.ylabel('Expected Return')
    plt.xlabel('StDev')
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename, format='pdf')

    return na_weights


def optimize(start_date, end_date, ls_symbols, ref_symbol,
             filename="portfoliovCAC40.pdf", ls_names=[], target_return=0.02):
    """
    @param ls_symbols candidates equities
    @param ref_symbol reference

    @return alloc allocation of equities
    """

    optimized_allocation = get_frontier(basic_portfolio, ref_symbol,
                                        ls_names, filename, target_return)

    plot_portfolio_vs_referance(start_date, end_date, ls_symbols,
                                optimized_allocation, ref_symbol)


def test_small_portfolio():
    symbols = ["AIR.PA", "LG.PA", "GLE.PA", "DG.PA"]
    ref_symbol = '^FCHI'
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365)
    optimize(start_date, end_date, symbols, ref_symbol, filename=None, target_return=0.012)


def test_cac40_portfolio():
    ref_symbol = '^FCHI'
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365)

    cac40_names = load_valid_cac40_names()

    optimize(start_date, end_date, cac40_names.index, ref_symbol,
             filename="EquitiesvFrontier2015.pdf", ls_names=cac40_modified.index)


if __name__ == '__main__':
    test_small_portfolio()
    # test_cac40_portfolio()
