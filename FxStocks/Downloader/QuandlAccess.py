import quandl
import datetime

RETURN_CSV = 'CSV'
RETURN_PANDAS = 'pandas'

class QuandlAccess():
    def __init__(self, quandl_key):
        quandl.ApiConfig.api_key = quandl_key

    def quandl_stocks(self, symbol, start_date=(2000, 1, 1), end_date=None):
        """
        symbol is a string representing a stock symbol, e.g. 'AAPL'
     
        start_date and end_date are tuples of integers representing the year, month,
        and day
     
        end_date defaults to the current date when None
        """
        query_list = []
        temp_query_list = []
        if isinstance(symbol, (list, tuple)):
            for single_symbol in symbol:
                temp_query_list = ['WIKI' + '/' + single_symbol + '.' + str(k) for k in range(1, 13)]
                query_list = query_list + temp_query_list
        else:
            query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]
     
        start_date = datetime.date(*start_date)
     
        if end_date:
            end_date = datetime.date(*end_date)
        else:
            end_date = datetime.date.today()
     
        return quandl.get(query_list, 
                returns='pandas', 
                start_date=start_date,
                end_date=end_date,
                collapse='daily',
                order='asc',
                transform='rdiff'
                )
     
    def quandl_simple_stocks(symbol):
    	quandl.get('WIKI/' + symbol)
 
if __name__ == '__main__':
 
    #apple_data = quandl_stocks('AAPL')
    #print(apple_data)

	stock_data = quandl_stocks('AAPL',(2017, 1, 1))
	#stock_data = quandl_simple_stocks('AAPL')
	print(stock_data.tail())
	stock_data.plot()
