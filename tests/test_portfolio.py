"""
Thi file contains test for the portfolio analysis.
"""

import datetime as dt
import pandas as pd
from portfolio_correlation import get_correlations
from portfolio_analyzer import analyze


start_date = dt.datetime(2011, 12, 1)
end_date = dt.datetime(2011, 12, 31)
symbols = ['AAPL', 'IBM', 'MSFT']


def test_get_correlations():
    correlations = get_correlations(start_date, end_date, symbols)
    assert isinstance(correlations, pd.DataFrame)
    assert correlations.shape == (3, 3)


def test_analyze():
    vol, ave_daily_ret, sharpe, cum_ret = \
        analyze(start_date, end_date, symbols, [0.1, 0.4, 0.5], debug=True)
    eps = 0.0001
    assert abs(vol - 0.00941707081886) * 100 < eps
    assert abs(sharpe - 0.561924531129) * 100 < eps
    assert abs(ave_daily_ret - 0.000333344702654) * 10000 < eps
    assert abs(cum_ret - 1.00608928693) * 10000 < eps


if __name__ == '__main__':
    test_get_correlations()
    test_analyze()
