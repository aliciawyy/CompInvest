"""
This file stores some basic information class.
"""
import numpy as np
import matplotlib.pyplot as plt
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
        @return list of individual stock prices arranged as a matrix
        or a DataFrame, e.g.
        Date        Stock A    Stock B     ...    Stock X
        2011-12-01  121.3       12.2       ...      43.1
        2011-12-02  123.1       13.1       ...      41.2
        ...
        2011-12-31
        """
        if self._close_prices is None:
            self._close_prices = load_stock_close_price(self.start_date, self.end_date,
                                                        self.tickers, source)
        return self._close_prices

    def print_information(self):
        print 'List of stock tickers:', self.tickers
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

    def get_portfolio_normalized_price(self, allocation, source='yahoo'):
        """
        @param source: source to get the data
        @param allocation: allocation = [allocation_stock_A, allocation_stock_B, ...,
                                            allocation_stock_X]
        @return: portfolio's normalized price
        """
        assert len(allocation) == len(self.tickers)
        if self._close_prices is None:
            self.get_stock_close_prices(source)
        normalized_prices = self._close_prices.values / self._close_prices.values[0, :]
        portfolio_normalized_price = np.sum(normalized_prices * allocation, axis=1)
        return portfolio_normalized_price

    def plot_with_reference(self, allocation, reference_ticker, source='yahoo', filename=None):
        """
        Plot the portfolio with given allocation along with a reference
        @param allocation: allocation of the stocks
        @param reference_ticker:
        @param source: source to get the market data
        @param filename: if filename is None, will show the plot screen, otherwise a pdf will be
        saved in the repository result/ with given name
        @return:
        """
        portfolio_normalized_price = self.get_portfolio_normalized_price(allocation, source)

        ref_close_price = load_stock_close_price(self.start_date, self.end_date,
                                                 [reference_ticker], source)
        ref_normalized_price = ref_close_price.values / ref_close_price.values[0, :]

        plt.clf()
        plt.plot(self._close_prices.index, portfolio_normalized_price)
        plt.plot(ref_close_price.index, ref_normalized_price)
        plt.legend(['Portfolio', reference_ticker])
        plt.ylabel('Normalized Close Price')
        plt.xlabel('Date')
        if filename is None:
            plt.show()
        else:
            path = './result/'
            plt.savefig(path + filename, format='pdf')
