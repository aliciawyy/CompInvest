# Third Party import
import datetime as dt

from load.load_ticker import load_valid_cac40_names
from portfolio_analyzer import plot_portfolio_vs_referance
from portfolio_frontier import get_frontier
from portfolio import BasicPortfolio


class BackTest(object):
    """
    The objective of this class is to make a back test with a target portfolio decided
    one year in advance then to test it in the current year

    |------------------------|-------------------|
         strategy period          test period
    """

    def __init__(self, ls_symbols, ref_symbol='^FCHI', end_date=dt.datetime.today(),
                 interval_days=365, ls_symbol_names=[]):
        self.symbols = ls_symbols
        self.symbol_names = self.symbols if len(ls_symbol_names) == 0 else ls_symbol_names
        self.reference_symbol = ref_symbol
        self.end_date = end_date
        self.mid_date = self.end_date - dt.timedelta(days=interval_days)
        self.start_date = self.mid_date - dt.timedelta(days=interval_days*1.5)

    def testing(self, target_return=0.011):
        """
        The method of back testing
        @param target_return: target return of the portfolio
        """
        best_allocation = get_frontier(BasicPortfolio(self.symbols, self.start_date,
                                                      self.mid_date, self.symbol_names),
                                       self.reference_symbol, filename=None,
                                       target_return=target_return)

        plot_portfolio_vs_referance(BasicPortfolio(self.symbols, self.start_date,
                                                   self.mid_date, self.symbol_names),
                                    best_allocation,
                                    self.reference_symbol,
                                    filename='result/portvCAC40-target.before.pdf')

        plot_portfolio_vs_referance(BasicPortfolio(self.symbols, self.mid_date,
                                                   self.end_date, self.symbol_names),
                                    best_allocation,
                                    self.reference_symbol,
                                    filename='result/portvCAC40-target.forecast.pdf')


def backtest_small_french_portfolio():
    """
    Test a small portfolio with four stocks
    """
    symbols = ["AIR.PA", "LG.PA", "GLE.PA", "DG.PA"]
    end_date = dt.datetime.today() - dt.timedelta(days=100)
    backtest_obj = BackTest(symbols, end_date=end_date)
    backtest_obj.testing(0.01)


def backtest_cac40():
    cac40_orig = load_valid_cac40_names()
    end_date = dt.datetime.today() - dt.timedelta(days=100)
    backtest_obj = BackTest(cac40_orig.index, end_date=end_date, ls_symbol_names=cac40_orig.values)
    backtest_obj.testing(0.01)


if __name__ == '__main__':
    backtest_small_french_portfolio()
    #backtest_cac40()
