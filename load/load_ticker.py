"""
This file contains the functions to load lists of tickers.

@author Alicia Wang
@date 4 oct 2014
"""
import os
import pandas as pd
from pandas import Series


def load_ticker_list(filename):
    """
    @type filename: path + filename where the csv file is
    """
    ticker_list = pd.read_csv(filename, header=False, sep='\t')
    return ticker_list


def load_cac40_names():
    """
    @return cac40 stored in a Series object with _Ticker_ as index
    and Equity's _Name_ as value
    """

    filename = os.path.dirname(__file__) + '/info/cac40.csv'

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


def load_valid_cac40_names():
    """
    Only load the cac40 names possible to retrieve data for the current year
    """
    cac40 = load_cac40_names()
    cac40_valid = cac40.drop(['GSZ.PA', 'UL.PA'])
    return cac40_valid
