'''
This file contains some functions on correlation analysis.
We mainly compute the CAC 40 correlation matrix during the
current year.
'''
# Third Party import
import datetime as dt
import numpy as np

import pandas.io.data as web

from LoadTicker import LoadCAC40

# -------------------------------------------------------
def main():
    cac40_orig  = LoadCAC40()
    cac40_modif = cac40_orig.drop(['SAN.PA', 'UL.PA', 'ML.PA'])
    ref_symbol  = '^FCHI'
    
    endd        = dt.datetime.today()
    startd      = endd - dt.timedelta(days = 365)    
    
    all_data = web.get_data_yahoo(cac40_modif.index, startd, endd)
    
    price  = all_data['Adj Close']
    volume = all_data['Volume']

    # Compute the percent changes of the price
    returns = price.pct_change()
    returns.columns = cac40_modif.values
    
    # Compute the correlation matrix
    corrMat = returns.corr()
    
    corrEADS = returns.corrwith(returns['Airbus'])
    print np.argmin(corrEADS), corrEADS.min()
    
    corrMat.to_csv("CAC40corrMat.csv")
    
    
# -------------------------------------------------------
if __name__ == '__main__':
    main()