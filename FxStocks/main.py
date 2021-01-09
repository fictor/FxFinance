from FxStocks import FxStocks

if __name__ == "__main__":
    fs = FxStocks()
    #fs.load_csv()
    
    fs.download()
    # fs.to_csv()

    fs.process()
    
    fs.get_diff_over_period()
    fs.plot()