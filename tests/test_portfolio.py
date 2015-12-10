"""
Thi file contains test for the portfolio analysis.
"""

import datetime as dt
import pandas as pd
from portfolio_correlation import get_correlations
from portfolio_analyzer import analyze


start_date = dt.datetime(2014, 12, 1)
end_date = dt.datetime(2014, 12, 31)
symbols = ['AC.PA', 'BNP.PA', 'AIR.PA']
symbol_names = ['Accor', 'Bnp Paribas', 'Airbus']


def test_get_correlations():
    correlations = get_correlations(start_date, end_date, symbols, symbol_names)
    assert isinstance(correlations, pd.DataFrame)
    assert correlations.shape == (3, 3)


def test_analyze():
    vol, ave_daily_ret, sharpe, cum_ret = \
        analyze(start_date, end_date, symbols, [0.1, 0.4, 0.5], debug=True)
    eps = 0.0001
    assert abs(vol - 0.0181124420596) * 100 < eps
    assert abs(sharpe + 2.84983291126) * 100 < eps
    assert abs(ave_daily_ret + 0.00325159267419) * 10000 < eps
    assert abs(cum_ret - 0.924307817736) * 10000 < eps


if __name__ == '__main__':
    test_get_correlations()
    test_analyze()
