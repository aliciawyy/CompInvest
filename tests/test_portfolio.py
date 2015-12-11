"""
Thi file contains test for the portfolio analysis.
"""

import datetime as dt
import pandas as pd
from portfolio import BasicPortfolio

basic_portfolio = BasicPortfolio(['AAPL', 'IBM', 'MSFT'], dt.datetime(2011, 12, 1),
                                 dt.datetime(2011, 12, 31))


def test_get_correlations():
    correlations = basic_portfolio.get_correlations()
    assert isinstance(correlations, pd.DataFrame)
    assert correlations.shape == (3, 3)


def test_analyze():
    vol, ave_daily_ret, sharpe, cum_ret = \
        basic_portfolio.analyze([0.1, 0.4, 0.5], source='local', debug=True)
    eps = 0.0001
    assert abs(vol - 0.00941707081886) * 100 < eps
    assert abs(sharpe - 0.561924531129) * 100 < eps
    assert abs(ave_daily_ret - 0.000333344702654) * 10000 < eps
    assert abs(cum_ret - 0.00608928693) * 10000 < eps


if __name__ == '__main__':
    test_get_correlations()
    test_analyze()
