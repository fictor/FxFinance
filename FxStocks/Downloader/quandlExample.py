import quandl
import datetime
 
with open('quandlkey.txt', 'r') as quandl_key_file:
    quandl_key = quandl_key_file.read()

quandl.ApiConfig.api_key = quandl_key
 
def quandl_stocks(symbol, start_date=(2000, 1, 1), end_date=None):
    """
    symbol is a string representing a stock symbol, e.g. 'AAPL'
 
    start_date and end_date are tuples of integers representing the year, month,
    and day
 
    end_date defaults to the current date when None
    """
 
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
            order='asc'
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
