#import UKElection
#
#if __name__ == "__main__":
#    UKElection.ukelection()

from FxStocks import FxStocks
if __name__ == "__main__":
    with open('quandl_key.txt', 'r') as quandl_key_file:
        quandl_key = quandl_key_file.read()
    print ('quandl_key = ' + quandl_key)


    fs = FxStocks(quandl_key)
    #fs.load_csv()
    
    fs.download()
    #fs.to_csv()

    fs.process()
    
    fs.get_diff_over_period()
    fs.plot()