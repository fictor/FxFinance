
from EventPlot import EventPlot
from DataDownloader import DataDownloader

# for time series/maths
import pandas

# for plotting data
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

def ukelection():    
    # Learn about API authentication here: https://plot.ly/python/getting-started
    # Find your api_key here: https://plot.ly/settings/api
    plotly_username = "felix.clap"
    with open('plotly_key.txt', 'r') as plotly_key_file:
        plotly_api_key = plotly_key_file

    plotly.tools.set_credentials_file(username=plotly_username, api_key=plotly_api_key)

    ticker = 'GBPUSD' # will use in plot titles later (and for creating Plotly URL)

    ##### download market GBP/USD data from Quandl, Bloomberg or CSV file
    #source = "Bloomberg"
    source  = "Quandl"
    # source = "CSV"

    csv_file = None

    event_plot = EventPlot()
    
    data_downloader = DataDownloader()
    start_date = event_plot.parse_dates(['01/01/1975'])

    if source == 'Quandl':
        vendor_ticker = "BOE/XUDLUSS"
    elif source == 'Bloomberg':
        vendor_ticker = 'GBPUSD BGN Curncy'
    elif source == 'CSV':
        vendor_ticker = 'GBPUSD'
        csv_file = 'D:/GBPUSD.csv'

    spot = data_downloader.download_time_series(vendor_ticker, ticker, start_date[0], source, csv_file = csv_file)

    labour_wins = ['28/02/1974', '10/10/1974', '01/05/1997', '07/06/2001', '05/05/2005']
    conservative_wins = ['03/05/1979', '09/06/1983', '11/06/1987', '09/04/1992', '06/05/2010']

    # convert to more easily readable format
    labour_wins_d = event_plot.parse_dates(labour_wins)
    conservative_wins_d = event_plot.parse_dates(conservative_wins)

    # only takes those elections where we have data
    labour_wins_d = [d for d in labour_wins_d if d > spot.index[0].to_pydatetime()]
    conservative_wins_d = [d for d in conservative_wins_d if d > spot.index[0].to_pydatetime()]

    spot.index.name = 'Date'

    # number of days before and after for our event study
    pre = -20
    post = 20

    # calculate spot path during Labour wins
    labour_wins_spot = event_plot.event_study(spot, labour_wins_d, pre, post, mean_label = 'Labour Mean')

    # calculate spot path during Conservative wins
    conservative_wins_spot = event_plot.event_study(spot, conservative_wins_d, pre, post, mean_label = 'Conservative Mean')

    ##### Create separate plots of price action during Labour and Conservative wins
    xaxis = 'Days'
    yaxis = 'Index'
    source_label = "Source: @thalesians/BBG/Wikipedia"

    
    ###### Plot market reaction during Labour UK election wins
    ###### Using default color scheme

    title = ticker + ' during UK gen elect - Lab wins' + '<BR>' + source_label

    fig = Figure(data=event_plot.convert_df_plotly(labour_wins_spot),
                 layout=event_plot.create_layout(title, xaxis, yaxis)
    )

    py.plot(fig, filename='labour-wins-' + ticker)

    ###### Plot market reaction during Conservative UK election wins
    ###### Using varying shades of blue for each line (helped by colorlover library)

    title = ticker + ' during UK gen elect - Con wins ' + '<BR>' + source_label

    # also apply graduated color scheme of blues (from light to dark)
    # see http://moderndata.plot.ly/color-scales-in-ipython-notebook/ for details on colorlover package
    # which allows you to set scales
    fig = Figure(data=event_plot.convert_df_plotly(conservative_wins_spot, gradcolor='Blues', addmarker=False),
                 layout=event_plot.create_layout(title, xaxis, yaxis),
    )

    plot_url = py.plot(fig, filename='conservative-wins-' + ticker)

    import plotly.tools as tls

    tls.embed("https://plot.ly/~thalesians/245")

##### Plot market reaction during Conservative UK election wins
    ##### create a plot consisting of 3 subplots (from left to right)
    ##### 1. Labour wins, 2. Conservative wins, 3. Conservative/Labour mean move

    # create a dataframe which grabs the mean from the respective Lab & Con election wins
    mean_wins_spot = pandas.DataFrame()
    mean_wins_spot['Labour Mean'] = labour_wins_spot['Labour Mean']
    mean_wins_spot['Conservative Mean'] = conservative_wins_spot['Conservative Mean']

    fig = plotly.tools.make_subplots(rows=1, cols=3)

    # apply different color scheme (red = Lab, blue = Con)
    # also add markets, which will have varying levels of opacity
    fig['data'] += Data(
        event_plot.convert_df_plotly(conservative_wins_spot, axis_no=1, 
                                     color_def=['blue'], addmarker=True) +
        event_plot.convert_df_plotly(labour_wins_spot, axis_no=2, 
                                     color_def=['red'], addmarker=True) +
        event_plot.convert_df_plotly(mean_wins_spot, axis_no=3, 
                                     color_def=['red', 'blue'], addmarker=True, showlegend = False)
                        )
        
    fig['layout'].update(title=ticker + ' during UK gen elects by winning party ' + '<BR>' + source_label)

    # use the scheme from https://plot.ly/python/bubble-charts-tutorial/
    # can use dict approach, rather than specifying each separately
    axis_style = dict(
            gridcolor='#FFFFFF',  # white grid lines
            ticks='outside',      # draw ticks outside axes
            ticklen=8,            # tick length
            tickwidth=1.5         #   and width
        )

    # create the various axes for the three separate charts
    fig['layout'].update(xaxis1=plotly.graph_objs.XAxis(axis_style, title=xaxis))
    fig['layout'].update(yaxis1=plotly.graph_objs.YAxis(axis_style, title=yaxis))

    fig['layout'].update(xaxis2=plotly.graph_objs.XAxis(axis_style, title=xaxis))
    fig['layout'].update(yaxis2=plotly.graph_objs.YAxis(axis_style))

    fig['layout'].update(xaxis3=plotly.graph_objs.XAxis(axis_style, title=xaxis))
    fig['layout'].update(yaxis3=plotly.graph_objs.YAxis(axis_style))

    fig['layout'].update(plot_bgcolor='#EFECEA')  # set plot background to grey

    plot_url = py.iplot(fig, filename='labour-conservative-wins-'+ ticker + '-subplot')

    import plotly.tools as tls

    tls.embed("https://plot.ly/~thalesians/246")