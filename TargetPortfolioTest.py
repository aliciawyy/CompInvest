'''
The objective of the function in this file is to make a back test with a target portfolio decided one year in advance then to test it in the current year

|------------------------|-------------------|
     strategy period          test period

@author Alicia Wang
@date 5 oct 2014
'''

# QSTK Imports
import QSTK.qstkutil.tsutil as tsu


# Third Party import
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas.io.data as web

from load_ticker import load_cac40_names
from portfolio_frontier import get_frontier
from portfolio_optimizer import DrawPortfolioRef


#-----------------------------------------------------------
def main():
    '''main function'''
    
    example_symbols = ['AIR.PA', 'LG.PA', 'GLE.PA', 'DG.PA']
    ref_symbol      = '^FCHI' # CAC 40
    
    interval = 365;
    
    endd   = dt.datetime.today()
    midd   = endd - dt.timedelta(days = interval)
    startd = endd - dt.timedelta(days = interval*2.5)
    
    cac40_orig  = load_cac40_names()
    
    cac40_modif = cac40_orig.drop(['SAN.PA', 'UL.PA'])
    
    # Get the optimal allocation
    opt_alloc = get_frontier(startd, midd, cac40_modif.index, ref_symbol,
                             ls_names = cac40_modif.values,
                             filename = "CAC40-12to13july-target.016.pdf",
                             target_return = 0.016)
    
    DrawPortfolioRef(startd, midd, cac40_modif.index, ref_symbol,
                         opt_alloc, filename = "portfoliovCAC40-target.016before.pdf") 
    
    DrawPortfolioRef(midd, endd, cac40_modif.index, ref_symbol,
                     opt_alloc, filename = "portfoliovCAC40-target.016test.pdf")    

#----------------------------------------------------------
if __name__ == '__main__':
    main()