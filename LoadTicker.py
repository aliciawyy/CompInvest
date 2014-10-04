'''
@author Alicia Wang
@date 4 oct 2014
'''
import pandas as pd

#--------------------------------------------------------
def LoadTickerList(filename):
    tickerlist = pd.read_csv(filename, sep = ',')
    return tickerlist
    
#--------------------------------------------------------    
def LoadCAC40():
    
    filename = './data/cac40.csv'
    
    print '[info]Load the CAC 40 List from ', filename
    
    # The header is 'Symbol' and 'Name'
    cac40list = LoadTickerList(filename)
    
    for i in range(len(cac40list.Symbol)):
        cac40list.Symbol[i] = cac40list.Symbol[i].upper()

    return cac40list

#--------------------------------------------------------
def main():
    cac40list = LoadCAC40()
    print cac40list
    
#--------------------------------------------------------
if __name__ == '__main__':
    main()