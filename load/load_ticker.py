"""
This file contains the functions to load lists of tickers.

@author Alicia Wang
@date 4 oct 2014
"""
import pandas as pd
from pandas import Series


def load_ticker_list(filename):
    """
    @type filename: path + filename where the csv file is
    """
    try:
        ticker_list = pd.read_csv(filename, header=False, sep='\t')
    except IOError:
        print 'cannot read csv file at: ', filename
    return ticker_list


def load_cac40_names():
    """
    @return cac40 stored in a Series object with _Ticker_ as index
    and Equity's _Name_ as value
    """

    filename = '../data/cac40.csv'

    print '[info]Load the CAC 40 List from ', filename

    # The header is 'Symbol' and 'Name'
    cac40list = load_ticker_list(filename)

    for i in range(len(cac40list.Symbol)):
        cac40list.Symbol[i] = cac40list.Symbol[i].upper()

    # Store the result into a Series object
    cac40 = Series(cac40list.Name.values, index=cac40list.Symbol.values)
    cac40.index.name = 'Ticker'
    cac40.name = 'Name'

    return cac40
