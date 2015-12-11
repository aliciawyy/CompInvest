"""
This file contains some functions on correlation analysis.
We mainly compute the CAC 40 correlation matrix during the
current year.
"""
import datetime as dt
import pandas as pd

from load.load_ticker import load_valid_cac40_names
from portfolio import BasicPortfolio


def get_correlations_cac40(filename='result/correlationCAC40.csv', target_ticker=None):
    symbols = load_valid_cac40_names()
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365)
    basic_portfolio = BasicPortfolio(symbols.index, start_date, end_date, symbols.values)
    correlations = basic_portfolio.get_correlations()

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

if __name__ == '__main__':
    get_correlations_cac40(target_ticker='AF.PA')
