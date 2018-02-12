import quandl
import matplotlib.pyplot as plt
import pandas as pd

auth_token = 'QTxeC7MJ_NMJoFhfmMjG'

def MatPlotLibDemo():
    # Example Two:
    with open('quandlkey.txt', 'r') as quandl_key_file:
        auth_token = quandl_key_file.read()

    perth_silver = quandl.get("PERTH/SLVR_USD_M", authtoken = auth_token)

    # Convert to pandas dataframe:
    
    silver_df = pd.DataFrame(perth_silver)

    print(silver_df.head(6))
    print(silver_df.tail(6))

    plt.subplot(2, 1, 1)
    plt.plot(silver_df.index, silver_df['Bid Average'])

    plt.title(''' Perth Mint Monthly Prices For Silver (USD) \n''')

    plt.xticks(silver_df.index[0::75],[])
    plt.xlabel('\n Year')
    plt.ylabel('Avg. Bid Price  \n')

    plt.subplot(2, 1, 2)
    plt.plot(silver_df.index, silver_df['Ask Average'])


    plt.xlabel('\n Year')
    plt.ylabel('Avg. Ask Price \n')

    plt.show()



