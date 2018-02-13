#import quandl
#import datetime
#
#RETURN_CSV = 'CSV'
#RETURN_PANDAS = 'pandas'

from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

# Dow Jones
param = {
    'q': ".DJI", # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "1Y" # Period (Ex: "1Y" = 1 year)
}

class GoogleFinanceAccess():
    def __init__(self):
        pass

    def google_finance_stocks(self, symbol, start_date=(2000, 1, 1), end_date=None):
        """
        symbol is a string representing a stock symbol, e.g. 'AAPL'
     
        start_date and end_date are tuples of integers representing the year, month,
        and day
     
        end_date defaults to the current date when None
        """
        # Dow Jones
        param = {
            'q': "FB", # Stock symbol (ex: "AAPL")
            'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
            'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
            'p': "3M" # Period (Ex: "1Y" = 1 year)
        }

        # get price data (return pandas dataframe)
        df = get_price_data(param)
        print(df)
        return df

    def example_2(self):
        params = [
        # Dow Jones
        {
            'q': ".DJI",
            'x': "INDEXDJX",
        },
        # NYSE COMPOSITE (DJ)
        {
            'q': "NYA",
            'x': "INDEXNYSEGIS",
        },
        # S&P 500
        {
            'q': ".INX",
            'x': "INDEXSP",
        }
        ]
        period = "1Y"
        # get open, high, low, close, volume data (return pandas dataframe)
        df = get_prices_data(params, period)
        print(df)
        #            .DJI_Open  .DJI_High  .DJI_Low  .DJI_Close  .DJI_Volume  \
        # 2016-07-20   18503.12   18562.53  18495.11    18559.01    85840786
        # 2016-07-21   18582.70   18622.01  18555.65    18595.03    93233337
        # 2016-07-22   18589.96   18590.44  18469.67    18517.23    86803016
        # 2016-07-23   18524.15   18571.30  18491.59    18570.85    87706622
        # 2016-07-26   18554.49   18555.69  18452.62    18493.06    76807470
        # ...               ...        ...       ...         ...         ...


    def example_3(self):
        params = [
        # Dow Jones
        {
            'q': ".DJI",
            'x': "INDEXDJX",
        },
        # NYSE COMPOSITE (DJ)
        {
            'q': "NYA",
            'x': "INDEXNYSEGIS",
        },
        # S&P 500
        {
            'q': ".INX",
            'x': "INDEXSP",
        }
        ]
        period = "1Y"
        interval = 60*30 # 30 minutes
        # get open, high, low, close, volume time data (return pandas dataframe)
        df = get_prices_time_data(params, period, interval)
        print(df)
        #                      .DJI_Open  .DJI_High  .DJI_Low  .DJI_Close  .DJI_Volume  \
        # 2016-07-19 23:00:00   18503.12   18542.13  18495.11    18522.47            0
        # 2016-07-19 23:30:00   18522.44   18553.30  18509.25    18546.27            0
        # 2016-07-20 00:00:00   18546.20   18549.59  18519.77    18539.93            0
        # 2016-07-20 00:30:00   18540.24   18549.80  18526.99    18534.18            0
        # 2016-07-20 01:00:00   18534.05   18540.38  18507.34    18516.41            0
        # ...                        ...        ...       ...         ...          ...

        #query_list = []
        #temp_query_list = []
        #if isinstance(symbol, (list, tuple)):
        #    for single_symbol in symbol:
        #        temp_query_list = ['WIKI' + '/' + single_symbol + '.' + str(k) for k in range(1, 13)]
        #        query_list = query_list + temp_query_list
        #else:
        #    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]
        #
        #start_date = datetime.date(*start_date)
        #
        #if end_date:
        #    end_date = datetime.date(*end_date)
        #else:
        #    end_date = datetime.date.today()
        #
        #return quandl.get(query_list, 
        #        returns='pandas', 
        #        start_date=start_date,
        #        end_date=end_date,
        #        collapse='daily',
        #        order='asc',
        #        transform='rdiff'
        #        )
        #
    #def quandl_simple_stocks(symbol):
    #	quandl.get('WIKI/' + symbol)
 
#if __name__ == '__main__':
 
#    #apple_data = quandl_stocks('AAPL')
#    #print(apple_data)

#	stock_data = quandl_stocks('AAPL',(2017, 1, 1))
#	#stock_data = quandl_simple_stocks('AAPL')
#	print(stock_data.tail())
#	stock_data.plot()
