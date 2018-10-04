import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
style.use('ggplot')

ticker = 'ITG'
start = dt.datetime(2018,1,1)
end = dt.datetime.now()

df = web.DataReader(ticker, 'yahoo', start, end)
df.to_csv('{}.csv'.format(ticker))

# Preprocess
df = pd.read_csv('{}.csv'.format(ticker), parse_dates=True, index_col=0)
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean() # 100 moving average

df_ohlc = df['Adj Close'].resample('10D').ohlc() # Take ohlc every 10 days
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)


# Plotting
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values,  width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()
