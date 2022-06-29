from matplotlib import ticker
from nsepy import get_history
from datetime import date
import datetime
import matplotlib
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

start = datetime.datetime(2022, 1, 1)
end = datetime.datetime(2022, 1, 31)

data = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]
labels = data.loc[[124,126,127]]
print(data.loc[[124,125,126,127]])
allocation_pct =[.1,.2,.3,.4]


# print(labels)
fig = go.Figure(data=[go.Pie(labels=labels, values=allocation_pct) ])
fig.update_layout(title_text="NSE F&O Stock List")
fig.show()
