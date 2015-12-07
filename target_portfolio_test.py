# Third Party import
import datetime as dt

from load.load_ticker import load_cac40_names
from portfolio_analyzer import plot_portfolio_vs_referance
from portfolio_frontier import get_frontier


class BackTest(object):
    """
    The objective of this class is to make a back test with a target portfolio decided
    one year in advance then to test it in the current year

    |------------------------|-------------------|
         strategy period          test period
    """

    symbol_names = symbols = []
    # CAC 40
    reference_symbol = '^FCHI'

    start_date = mid_date = end_date = dt.datetime.today()

    def __init__(self, ls_symbols, ref_symbol='^FCHI', end_date=dt.datetime.today(),
                 interval_days=365, ls_symbol_names=[]):
        self.symbols = ls_symbols
        if len(ls_symbol_names) == 0:
            self.symbol_names = self.symbols
        else:
            self.symbol_names = ls_symbol_names
        self.reference_symbol = ref_symbol
        self.end_date = end_date
        self.mid_date = self.end_date - dt.timedelta(days=interval_days)
        self.start_date = self.mid_date - dt.timedelta(days=interval_days*1.5)

    def testing(self, target_return=0.011):
        """
        The method of backtesting
        @param target_return: target return of the portfolio
        """
        best_allocation = get_frontier(self.start_date, self.mid_date, self.symbols,
                                       self.reference_symbol,ls_names=self.symbol_names,
                                       filename=None, target_return=target_return)

        plot_portfolio_vs_referance(self.start_date, self.mid_date, self.symbols, best_allocation,
                                    self.reference_symbol, filename="portvCAC40-target.before.pdf")

        plot_portfolio_vs_referance(self.mid_date, self.end_date, self.symbols, best_allocation,
                                    self.reference_symbol, filename="portvCAC40-target.forecast.pdf")


def backtest_small_french_portfolio():
    """
    Test a small portfolio with four stocks
    """
    symbols = ["AIR.PA", "LG.PA", "GLE.PA", "DG.PA"]
    end_date = dt.datetime.today() - dt.timedelta(days=100)
    backtest_obj = BackTest(symbols, end_date=end_date)
    backtest_obj.testing(0.01)


def backtest_cac40():
    cac40_orig = load_cac40_names()
    cac40_modified = cac40_orig.drop(['SAN.PA', 'UL.PA', 'GSZ.PA'])
    end_date = dt.datetime.today() - dt.timedelta(days=100)
    backtest_obj = BackTest(cac40_modified, end_date=end_date)
    backtest_obj.testing(0.01)


if __name__ == '__main__':
    backtest_small_french_portfolio()
    #backtest_cac40()
