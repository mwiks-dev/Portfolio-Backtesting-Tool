import numpy as np
import pandas as pd
import pandas_datareader as web
import plotly.express as px
import pandas_datareader
import datetime
import pandas_datareader.data as web
import plotly.graph_objects as go

start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2020, 10, 30)
AAPL = web.DataReader('AAPL','yahoo',start,end)
FB = web.DataReader('FB','yahoo',start,end)
MSFT = web.DataReader('MSFT','yahoo',start,end)
CRM = web.DataReader('CRM','yahoo',start,end)

##Banchmark SPY for comparision
SPY = web.DataReader('SPY','yahoo',start,end)

#Portfolio Asset Allocation. 
labels = ['AAPL','FB','MSFT','CRM']
allocation_pct = [.2,.3,.4,.1]

fig = go.Figure(data=[go.Pie(labels=labels, values=allocation_pct)])
fig.update_layout(title="Portfolio Asset Allocation")
fig.show()

# Calculate the cumulative return
for df in (AAPL,FB,MSFT,CRM,SPY): 
  df['Cum Return'] = df['Adj Close']/df.iloc[0]['Adj Close']

AAPL.head()