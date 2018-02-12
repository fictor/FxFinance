
stock_list=['AAPL','AMZN','MSFT']

from Downloader.QuandlAccess import QuandlAccess
import pandas as pd

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

days = mdates.DayLocator(interval=7)   # every week
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y/%m')

class FxStocks():

    def __init__(self,quandl_key):
        self.start_date = (2018, 1, 1)
        self.quandl_key = quandl_key

    def load_csv(self):
        self.stock_df = pd.DataFrame.from_csv('stock.csv')

    def download(self):
        stock_df_list = []
        #for stock in stock_list:
        QuandlAccess(self.quandl_key)
        self.stock_df = QuandlAccess.quandl_stocks(stock_list,self.start_date)

    def process(self):
        self.used_column = [s for s in self.stock_df.columns.values if "Open" in s and not 'Adj' in s]
        #print(self.stock_df.tail())

    def get_diff_over_period(self):
        print_diff_over_period = self.stock_df.last_valid_index() - self.stock_df.first_valid_index()
        print(print_diff_over_period)

        print_diff_over_period = self.stock_df[self.used_column].iloc[-1] - self.stock_df[self.used_column].iloc[1]
        print(print_diff_over_period)

    def plot(self):
        stock_df = self.stock_df
        ##print(stock_df.head(6))
        ##print(stock_df.tail(6))

        ax = plt.subplot(1, 1, 1)
        print(list(stock_df.columns.values))
        #print(list(stock_df))
        print(self.used_column)
        index = 0
        for single_stock_df_column in self.used_column:
            cur_plot = plt.plot(stock_df.index, stock_df[single_stock_df_column], label=stock_list[index]) # , stock_df['Open']
            index +=1
        plt.plot(stock_df.index, stock_df[self.used_column].mean(axis='columns'), label='mean')
        plt.legend(shadow=True, fancybox=True)
        plt.title('Stock Analysis') #self.used_column

        #fig, ax = plt.subplots()
        #ax.plot(date, r.adj_close)
        # format the ticks

        #ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(yearsFmt)
        #ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_minor_locator(days)

        #ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))   #to get a tick every 15 minutes
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))     #optional formatting 


        datemin = datetime.date(*self.start_date)
        datemax = datetime.date.today()
        #datemin = datetime.date(date.min().year, 1, 1)
        #datemax = datetime.date(date.max().year + 1, 1, 1)
        ax.set_xlim(datemin, datemax)

        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

        # format the coords message box
        #def price(x):
        #    return '$%1.2f' % x
        #ax.format_ydata = price
        #ax.grid(True)

        fig = plt.figure(1)
        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()

        #plt.xticks(stock_df.index, rotation='vertical')
        plt.xlabel('Date')
        plt.ylabel('Open Price (\%)')

        plt.tight_layout()

        ## Pad margins so that markers don't get clipped by the axes
        #plt.margins(0.2)
        #
        ## Tweak spacing to prevent clipping of tick-labels
        #plt.subplots_adjust(bottom=0.3) #0.15)

        #plt.tight_layout()
        #plt.subplot(2, 1, 2)
        #plt.plot(stock_df.index, stock_df['Ask Average'])
        #
        #
        #plt.xlabel('\n Year')
        #plt.ylabel('Avg. Ask Price \n')

        #legend(framealpha=0.5)

        plt.show()

    def to_csv(self):
        self.stock_df.to_csv('stock.csv')