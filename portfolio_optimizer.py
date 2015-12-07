"""
This file will store the function which can optimize a portfolio
based on a selection of equities and their result for a chosen
period

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
from portfolio_analyzer import get_daily_return0, plot_portfolio_vs_referance


def optimize(start_date, end_date, ls_symbols, ref_symbol,
             filename="portfoliovCAC40.pdf", ls_names=[]):
    """
    @param ls_symbols candidates equities
    @param ref_symbol reference

    @return alloc allocation of equities
    """

    stock_close_prices = load_stock_close_price(start_date, end_date, ls_symbols)

    stock_normalized_price = stock_close_prices.values / stock_close_prices.values[0, :]

    daily_return0 = get_daily_return0(stock_normalized_price)

    # Special Case with fTarget=None, just returns average rets.
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

    plt.clf()
    plt.plot(lf_std, lf_returns, 'b')

    if len(ls_names) == 0:
        ls_names = ls_symbols

    # Plot individual stock risk/return as green +
    for i, f_ret in enumerate(na_avgrets):
        plt.plot(na_std[i], f_ret, 'g+')
        plt.text(na_std[i], f_ret, ls_names[i])

    plt.title('Efficient Frontier For CAC 40')
    plt.legend(['Frontier'], loc='lower left')
    plt.ylabel('Expected Return')
    plt.xlabel('StDev')
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename, format='pdf')

    plot_portfolio_vs_referance(start_date, end_date, ls_symbols,
                                lna_portfolios[81], ref_symbol)


def test_small_portfolio():
    symbols = ["AIR.PA", "LG.PA", "GLE.PA", "DG.PA"]
    ref_symbol = '^FCHI'
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365)
    optimize(start_date, end_date, symbols, ref_symbol, filename=None)


def test_cac40():
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365)

    cac40_orig = load_cac40_names()
    cac40_modif = cac40_orig.drop(['SAN.PA', 'UL.PA', 'GSZ.PA'])
    ref_symbol = '^FCHI'

    optimize(start_date, end_date, cac40_modif.index, ref_symbol,
             filename=None, ls_names=cac40_modif.index)


if __name__ == '__main__':
    test_small_portfolio()
    test_cac40()
