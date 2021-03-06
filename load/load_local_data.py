"""
This is to get the data locally
@author Alicia Wang
@date 5 oct 2014
"""

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt


def load_local_data_from_yahoo(start_date, end_date, ls_symbols):
    """Get the data from local QSTK directory"""
    ldt_timestamps = du.getNYSEdays(start_date, end_date,
                                    dt.timedelta(hours=16))

    return load_local_data(ldt_timestamps, ls_symbols)


def load_local_data(ldt_timestamps, ls_symbols, source = 'Yahoo'):
    """Get the data from local QSTK directory
    @return a dict object of data well cleaned
    """

    # Define the keys
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    data_obj = da.DataAccess(source)
    ldf_data = data_obj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    # Range the data
    d_data = dict(zip(ls_keys, ldf_data))

    # Clean all the data
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    return d_data
