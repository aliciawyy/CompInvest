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
from load_ticker import load_cac40_names
from load_data import load_stock_close_price
from portfolio_analyzer import get_daily_return0


def get_frontier(startdate, enddate, ls_symbols, ref_symbol,
                 ls_names=[], filename="EquitiesvFrontier.pdf",
                 target_return=0.015):
    """
    @param ls_symbols candidates equities
    @param ls_names   candidates names
    @param ref_symbol reference
    """

    stock_close_price = load_stock_close_price(startdate, enddate, ls_symbols)

    stock_normalized_price = stock_close_price.values / stock_close_price.values[0, :]

    ref_close_price = load_stock_close_price(startdate, enddate, [ref_symbol])
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

    for i in range(len(na_weights)):
        if abs(na_weights[i]) > 0.00001:
            print ls_names[i], ':', na_weights[i]

    plt.clf()

    fig = plt.figure(figsize=(8, 10), dpi=100)

    # Plot individual stock risk/return as green +
    for i in range(len(ls_symbols)):
        #        plt.plot(na_std[i], f_ret, 'g+')
        #        plt.text(na_std[i], f_ret, ls_names[i], fontsize = 10)
        ave = np.average(daily_return0[:, i])
        std = np.std(daily_return0[:, i])
        plt.plot(std, ave, 'g+')
        plt.text(std, ave, ls_names[i], fontsize=5)

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
    plt.savefig(filename, format='pdf')

    return na_weights


def test_cac40_portfolio():
    # symbols = ['AIR.PA', 'LG.PA', 'GLE.PA', 'DG.PA']
    ref_symbol = '^FCHI'

    endd = dt.datetime.today()
    startd = endd - dt.timedelta(days=365 * 2)

    cac40_orig = load_cac40_names()

    cac40_modif = cac40_orig.drop(['SAN.PA', 'UL.PA', 'GSZ.PA'])

    get_frontier(startd, endd, cac40_modif.index, ref_symbol,
                 filename="EquitiesvFrontier2015.pdf",
                 ls_names=cac40_modif.values)


if __name__ == '__main__':
    test_cac40_portfolio()