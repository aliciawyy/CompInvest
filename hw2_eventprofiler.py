"""
This is a learning version of the homework II - The Event Profiler
@author Alicia Wang
@date 5 oct 2014
"""

# QSTK Imports
import QSTK.qstkutil.DataAccess as da
# Third Party Imports
import datetime as dt
from portfolio import BasicPortfolio


def main():
    """Main Function"""

    # Construct the two symbol lists SP 500 of 2008 and 2012
    dataobj = da.DataAccess('Yahoo')
    symbols08 = dataobj.get_symbols_from_list("sp5002008")
    symbols08.append('SPY')

    symbols12 = dataobj.get_symbols_from_list("sp5002012")
    symbols12.append('SPY')

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)

    basic_portfolio08 = BasicPortfolio(symbols08, start_date, end_date)
    basic_portfolio08.event_profiler(source='local', filename="MyEventStudy08.9.chg.pdf")
    basic_portfolio12 = BasicPortfolio(symbols12, start_date, end_date)
    basic_portfolio12.event_profiler(source='local', filename="MyEventStudy12.9.chg.pdf")


if __name__ == '__main__':
    main()
