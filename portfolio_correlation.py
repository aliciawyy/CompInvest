"""
This file contains some functions on correlation analysis.
We mainly compute the CAC 40 correlation matrix during the
current year.
"""
import datetime as dt
import pandas as pd

from load.load_ticker import load_valid_cac40_names
from load.load_data import load_stock_close_price


def get_correlations_cac40(filename='result/correlationCAC40.csv', target_ticker=None):
    symbols = load_valid_cac40_names()
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365)
    correlations = get_correlations(start_date, end_date, symbols.index, symbols.values)

    if isinstance(correlations, pd.DataFrame):
        print 'Write the correlation matrix into file: ', filename
        correlations.to_csv(filename)

    if target_ticker is not None and target_ticker in symbols.index:
        ticker_name = symbols[target_ticker]
        target_correlation = correlations[ticker_name]
        target_correlation = target_correlation.drop(ticker_name)
        print 'The stock %s is least correlated to %s with correlation %f' % \
              (ticker_name, target_correlation.argmin(), target_correlation.min())
        print 'The stock %s is most correlated to %s with correlation %f' % \
              (ticker_name, target_correlation.argmax(), target_correlation.max())


def get_correlations(start_date, end_date, symbols, symbol_names=[]):
    """
    Get the correlation matrix of a given list of symbols
    @param start_date: start date of analysis
    @param end_date: end date of analysis
    @param symbols: symbol list
    @param symbol_names: more explicit names of the symbols
    @return: Correlation matrix
    """

    prices = load_stock_close_price(start_date, end_date, symbols)
    returns = prices.pct_change()
    symbol_names = symbols if len(symbol_names) is 0 else symbol_names
    returns.columns = symbol_names
    correlation_matrix = returns.corr()
    return correlation_matrix


if __name__ == '__main__':
    get_correlations_cac40(target_ticker='AF.PA')
