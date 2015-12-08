"""
This file contains unittests for the loading functions in
.load
"""

import datetime as dt

from load.load_ticker import load_cac40_names
from load.load_local_data import load_local_data_from_yahoo
from load.load_data import load_stock_close_price


def test_load_cac40_names():
    cac40list = load_cac40_names()
    assert cac40list.size > 1
    assert cac40list.index.name == 'Ticker'
    assert cac40list.name == 'Name'


def test_load_local_data_from_yahoo():
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    ls_symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    local_data = load_local_data_from_yahoo(start_date, end_date, ls_symbols)
    assert local_data['close'].shape == (252, 4)


def test_load_stock_close_price():
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    ls_symbols = ['AAPL', 'GLD', 'XOM']
    stock_close_prices = load_stock_close_price(start_date, end_date, ls_symbols, 'yahoo')
    assert stock_close_prices.shape == (252, 3)
    assert len(stock_close_prices['AAPL']) == 252
    local_close_prices = load_stock_close_price(start_date, end_date, ls_symbols, 'local')
    assert local_close_prices.shape == (252, 3)


if __name__ == '__main__':
    test_load_cac40_names()
    test_load_local_data_from_yahoo()
    test_load_stock_close_price()
