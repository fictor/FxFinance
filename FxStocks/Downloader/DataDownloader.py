
# for time series manipulation
import pandas

class DataDownloader:
    def __init__(self, quandl_key):
        self.quandl_key = quandl_key

    def download_time_series(self, vendor_ticker, pretty_ticker, start_date, source, csv_file = None):

        if source == 'Quandl':
            import quandl
            # Quandl requires API key for large number of daily downloads
            # https://www.quandl.com/help/api
            quandl.ApiConfig.api_key = self.quandl_key
            spot = quandl.get(vendor_ticker)    # Bank of England's database on Quandl
            spot = pandas.DataFrame(data=spot['Value'], index=spot.index)
            spot.columns = [pretty_ticker]

        elif source == 'Bloomberg':
            from bbg_com import HistoricalDataRequest
            req = HistoricalDataRequest([vendor_ticker], ['PX_LAST'], start = start_date)
            req.execute()

            spot = req.response_as_single()
            spot.columns = [pretty_ticker]
        elif source == 'CSV':
            dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d')

            # in case you want to use a source other than Bloomberg/Quandl
            spot = pandas.read_csv(csv_file, index_col=0, parse_dates=0, date_parser=dateparse)

        return spot