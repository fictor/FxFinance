from pandas_datareader import data as pdr

import datetime
import pandas as pd

import fix_yahoo_finance as yf

class FixYahooFinanceAccess():

    def get_stock_test(self, symbols, start_date=(2000, 1, 1), end_date=None):
        yf.pdr_override() # <== that's all it takes :-)

        start_date = datetime.date(*start_date)
     
        if end_date:
            end_date = datetime.date(*end_date)
        else:
            end_date = datetime.date.today()

        start_date = start_date.strftime("%Y-%m-%d")

        end_date = end_date.strftime("%Y-%m-%d") #%Y-%m-%d %H:%M:%S

        #data = pdr.get_data_yahoo(symbols[0], start=start_date, end=end_date)
        #
        #if len(symbols) > 1:
        #    for symbol in symbols[1:]:
        #        temp_data = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        #        data = pd.concat([data, temp_data])
        # download dataframe
        #data1 = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2018-04-30")
        #data2 = pdr.get_data_yahoo("SHOP", start="2017-01-01", end="2018-04-30")
        #data3 = pdr.get_data_yahoo("AAPL", start="2017-01-01", end="2018-04-30")
        #
        #data = pd.concat([data1, data2, data3])

        # download Panel
        data = None
        retry = 0
        max_retry = 5
        while retry < max_retry and not isinstance(data, pd.DataFrame):
            try:
                data = pdr.get_data_yahoo(symbols, start=start_date, end=end_date, as_panel = False)
            except ValueError:  #raised if `y` is empty.
                data = None
            retry += 1

        # percentage of total
        #data = (data.div(data.sum())).multiply(100)

        data = data.pct_change().multiply(100)
        
        return data