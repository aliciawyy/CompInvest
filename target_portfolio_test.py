# Third Party import
import datetime as dt

from load_ticker import load_cac40_names
from portfolio_analyzer import plot_portfolio_vs_referance
from portfolio_frontier import get_frontier


def backtest_cac40():
    """
    The objective of the function in this file is to make a back test with a target portfolio decided
    one year in advance then to test it in the current year
    
    |------------------------|-------------------|
         strategy period          test period
    """
    
    ref_symbol = '^FCHI' # CAC 40
    
    interval = 365
    
    endd = dt.datetime.today()
    midd = endd - dt.timedelta(days=interval)
    startd = endd - dt.timedelta(days=interval*2.5)
    
    cac40_orig = load_cac40_names()
    cac40_modified = cac40_orig.drop(['SAN.PA', 'UL.PA', 'GSZ.PA'])
    
    # Get the optimal allocation
    opt_alloc = get_frontier(startd, midd, cac40_modified.index, ref_symbol,
                             ls_names=cac40_modified.values,
                             filename=None,
                             target_return=0.011)
    
    plot_portfolio_vs_referance(startd, midd, cac40_modified.index, opt_alloc, ref_symbol,
                                filename="portfoliovCAC40-target.before.pdf")
    
    plot_portfolio_vs_referance(midd, endd, cac40_modified.index, opt_alloc, ref_symbol,
                                filename="portfoliovCAC40-target.test.pdf")


if __name__ == '__main__':
    backtest_cac40()