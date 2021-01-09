from Downloader.FixYahooFinanceAccess import FixYahooFinanceAccess

import pandas as pd
import datetime 

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.widgets import Cursor

half_days = mdates.HourLocator(interval=12)   # every week
days = mdates.DayLocator()   # every week
weeks = mdates.DayLocator(interval=7)   # every week
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
daysFmt = mdates.DateFormatter('%d/%hd')
monthsFmt = mdates.DateFormatter('%m/%w')
yearsFmt = mdates.DateFormatter('%Y/%m')

class FxStocks():
    def __init__(self):
        self.start_date_tuple = (2020, 12, 15)
        self.start_date = datetime.date(*self.start_date_tuple) #*start_date)
        self.end_date = datetime.date.today()
        self.diff_date = self.end_date - self.start_date
        if (self.diff_date.days < 60):
            self.show_days = True
        else:
            self.show_days = False
        with open('stock_list.txt', 'r') as stock_list_file:
            self.stock_list = stock_list_file.read().splitlines()

    def load_csv(self):
        self.stock_df = pd.DataFrame.from_csv('stock.csv')

    def download(self):
        fyf = FixYahooFinanceAccess()
        self.stock_df = fyf.get_stock_test(self.stock_list,self.start_date_tuple)

    def process(self):
        self.used_column = [s for s in self.stock_df.columns.values if "Open" in s and not 'Adj' in s]

    def get_diff_over_period(self):
        print_diff_over_period = self.stock_df.last_valid_index() - self.stock_df.first_valid_index()
        print(print_diff_over_period)

        print_diff_over_period = self.stock_df[self.used_column].iloc[-1] - self.stock_df[self.used_column].iloc[1]
        print(print_diff_over_period)

        print('Getting SUM')
        print(self.stock_df[self.used_column].sum())

    def plot(self):
        stock_df = self.stock_df

        ax = plt.subplot(1, 1, 1)
        # print(list(stock_df.columns.values))
        # print(self.used_column)
        index = 0
        for single_stock_df_column in self.used_column:
            cur_plot = plt.plot(stock_df.index, stock_df[single_stock_df_column], label=single_stock_df_column[1])#)label=self.stock_list[index]) # , stock_df['Open']
            index +=1
        plt.plot(stock_df.index, stock_df[self.used_column].mean(axis='columns'), label='mean')
        plt.legend(shadow=True, fancybox=True)
        plt.title('Stock Analysis')

        #fig, ax = plt.subplots()
        #ax.plot(date, r.adj_close)
        # format the ticks
        if self.show_days:
            ax.xaxis.set_major_locator(days)
            ax.xaxis.set_minor_locator(half_days)
            ax.xaxis.set_major_formatter(daysFmt)
        else:
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_minor_locator(weeks)
            ax.xaxis.set_major_formatter(monthsFmt)
        ax.set_xlim(self.start_date, self.end_date)

        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

        #ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))   #to get a tick every 15 minutes
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))     #optional formatting 

        #datemin = datetime.date(*self.start_date_tuple)
        #datemax = datetime.date.today()


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
        plt.ylabel(r'Open Price (\%)')

        plt.tight_layout()

        # set useblit = True on gtkagg for enhanced performance
        cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

        print("Show")
        plt.show()

    def to_csv(self):
        self.stock_df.to_csv('stock.csv')