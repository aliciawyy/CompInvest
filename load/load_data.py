"""
This is the general interface to load data, either we want to
load the data from internet through panda or load local data through
QSTK for tests.
@author Alice Wang
"""
import pandas.io.data as web
from load_local_data import load_local_data_from_yahoo


def load_stock_close_price(start_date, end_date, ls_symbols, source='yahoo'):
    """
    @param start_date:
    @param end_date:
    @param ls_symbols:
    @param source:
    @return: The close prices of given symbols
    """
    if source == 'google':
        close_key = 'Close'
    elif source == 'yahoo':
        close_key = 'Adj Close'
    elif source == 'local':
        close_key = 'close'

    all_stock_data = load_all_stock_data(start_date, end_date, ls_symbols, source)
    stock_close_prices = all_stock_data[close_key]

    stock_close_prices = stock_close_prices.fillna(method='ffill')
    stock_close_prices = stock_close_prices.fillna(method='bfill')
    stock_close_prices = stock_close_prices.fillna(1.0)
    return stock_close_prices


def load_all_stock_data(start_date, end_date, ls_symbols, source='yahoo'):
    """
    @param start_date: start date of loading
    @param end_date: end date of loading
    @param ls_symbols: list of symbols
    @param source: source, to load from 'google', 'yahoo' or 'local'

    """
    acceptable_sources = frozenset(['google', 'yahoo', 'local'])
    if source not in acceptable_sources:
        raise ValueError('The given source %s is not in acceptable sources %s' % (
            source, str(acceptable_sources)))

    if source == 'local':
        all_stock_data = load_local_data_from_yahoo(start_date, end_date, ls_symbols)
    else:
        all_stock_data = web.DataReader(ls_symbols, source, start=start_date, end=end_date)

    return all_stock_data
