
# for dates
import datetime

# time series manipulation
import pandas

# for plotting data
import plotly
from plotly.graph_objs import *

class EventPlot():
    def __init__(self):
        pass
    def event_study(self, spot, dates, pre, post, mean_label = 'Mean'):
        # event_study - calculates the asset price moves over windows around event days
        #
        # spot = price of asset to study
        # dates = event days to anchor our event study
        # pre = days before the event day to start our study
        # post = days after the event day to start our study
        #

        data_frame = pandas.DataFrame()

        # for each date grab spot data the days before and after
        for i in range(0, len(dates)):
            mid_index = spot.index.searchsorted(dates[i])
            start_index = mid_index + pre
            finish_index = mid_index + post + 1

            x = (spot.ix[start_index:finish_index])[spot.columns.values[0]]

            data_frame[dates[i]] = x.values

        data_frame.index = range(pre, post + 1)

        data_frame = data_frame / data_frame.shift(1) - 1   # returns

        # add the mean on to the end
        data_frame[mean_label] = data_frame.mean(axis=1)

        data_frame = 100.0 * (1.0 + data_frame).cumprod()   # index
        data_frame.ix[pre,:] = 100

        return data_frame

    def parse_dates(self, str_dates):
        # parse_dates - parses string dates into Python format
        #
        # str_dates = dates to be parsed in the format of day/month/year
        #

        dates = []

        for d in str_dates:
            dates.append(datetime.datetime.strptime(d, '%d/%m/%Y'))

        return dates

    def create_layout(self, title, xaxis, yaxis, width = -1, height = -1):
        # create_layout - populates a layout object
        # title = title of the plot
        # xaxis = xaxis label
        # yaxis = yaxis label
        # width (optional) = width of plot
        # height (optional) = height of plot
        #

        layout = Layout(
                    title = title,
                    xaxis = plotly.graph_objs.XAxis(
                        title = xaxis,
                        showgrid = False
                ),
                    yaxis = plotly.graph_objs.YAxis(
                        title= yaxis,
                        showline = False
                )
            )

        if width > 0 and height > 0:
            layout['width'] = width
            layout['height'] = height

        return layout

    def convert_df_plotly(self, dataframe, axis_no = 1, color_def = ['default'],
                          special_line = 'Mean', showlegend = True, addmarker = False, gradcolor = None):
        # convert_df_plotly - converts a Pandas data frame to Plotly format for line plots
        # dataframe = data frame due to be converted
        # axis_no = axis for plot to be drawn (default = 1)
        # special_line = make lines named this extra thick
        # color_def = color scheme to be used (default = ['default']), colour will alternate in the list
        # showlegend = True or False to show legend of this line on plot
        # addmarker = True or False to add markers
        # gradcolor = Create a graduated color scheme for the lines
        #
        # Also see http://nbviewer.ipython.org/gist/nipunreddevil/7734529 for converting dataframe to traces
        # Also see http://moderndata.plot.ly/color-scales-in-ipython-notebook/

        x = dataframe.index.values

        traces = []

        # will be used for market opacity for the markers
        increments = 0.95 / float(len(dataframe.columns))

        if gradcolor is not None:
            try:
                import colorlover as cl
                color_def = cl.scales[str(len(dataframe.columns))]['seq'][gradcolor]
            except:
                print('Check colorlover installation...')

        i = 0

        for key in dataframe:
            scatter = plotly.graph_objs.Scatter(
                        x = x,
                        y = dataframe[key].values,
                        name = key,
                        xaxis = 'x' + str(axis_no),
                        yaxis = 'y' + str(axis_no),
                        showlegend = showlegend)

            # only apply color/marker properties if not "default"
            if color_def[i % len(color_def)] != "default":
                if special_line in str(key):
                    # special case for lines labelled "mean"
                    # make line thicker
                    scatter['mode'] = 'lines'
                    scatter['line'] = plotly.graph_objs.Line(
                                color = color_def[i % len(color_def)],
                                width = 2
                            )
                else:
                    line_width = 1

                    # set properties for the markers which change opacity
                    # for markers make lines thinner
                    if addmarker:
                        opacity = 0.05 + (increments * i)
                        scatter['mode'] = 'markers+lines'
                        scatter['marker'] = plotly.graph_objs.Marker(
                                    color=color_def[i % len(color_def)],  # marker color
                                    opacity = opacity,
                                    size = 5)
                        line_width = 0.2

                    else:
                        scatter['mode'] = 'lines'

                    scatter['line'] = plotly.graph_objs.Line(
                            color = color_def[i % len(color_def)],
                            width = line_width)
                    
                i = i + 1

            traces.append(scatter)

        return traces