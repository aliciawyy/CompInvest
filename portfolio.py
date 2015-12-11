"""
This file stores some basic information class.
"""
from load.load_data import load_stock_close_price


class BasicPortfolio(object):
    """
    Basic Portfolio information class
    """

    def __init__(self, ticker_list, start_date, end_date, ticker_names=None):
        self.tickers = ticker_list
        self.start_date = start_date
        self.end_date = end_date
        self.ticker_names = self.tickers if ticker_names is None else ticker_names
        self._close_prices = None

    def get_stock_close_prices(self, source='yahoo'):
        """
        Return the stock close prices of the current portfolio
        @param source: source to get the close price
        """
        if self._close_prices is None:
            self._close_prices = load_stock_close_price(self.start_date, self.end_date,
                                                        self.tickers, source)
        return self._close_prices

    def print_information(self):
        print 'List of stocks:', self.tickers
        print 'start date:', self.start_date
        print 'end date:', self.end_date

    def get_correlations(self):
        """
        Get the correlation matrix between the portfolio components's daily return vectors
        """
        prices = self.get_stock_close_prices()
        returns = prices.pct_change()
        returns.columns = self.ticker_names
        correlation_matrix = returns.corr()
        return correlation_matrix
