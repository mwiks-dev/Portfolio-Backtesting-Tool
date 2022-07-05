from operator import index
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
from pandas.tseries.offsets import MonthEnd
from sqlalchemy import create_engine



data = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]
data['SYMBOL'].to_csv('CSV/symbol.csv')
tickers = pd.read_csv('CSV/symbol.csv', header=None)[1].tolist()
tickers.pop(0)
tickerdata = []

# for ticker in tickers:
#     tickerdata.append(yf.download(ticker, start='2019-01-01', end='2019-12-31').reset_index())

engine = create_engine('postgresql://mwiks-dev:1455@localhost/nsehistory')

for frame, symbol in zip(tickerdata, tickers):
    frame.to_csv('CSV/' + symbol + '.csv', index=False)

for frame,symbol in zip(tickerdata, tickers):
    frame.to_sql(symbol, engine, index=False)

# print(pd.read_sql(f'SELECT "Date" ,"Adj Close" AS "{tickers[2]}" FROM "ACC"', engine))
df = pd.DataFrame()

for name in tickers:
    df = df.append(pd.read_sql(\
        f'SELECT "Date" ,"Adj Close" AS "{name}" FROM "{name}"', engine))

print(df)


# pd.read_csv('SELECT * FROM "ACC.csv"',('CSV/ACC.csv'))
# for ticker in tickers:
#     ticker_data = yf.download(ticker,start,end)
#     data = pd.DataFrame(ticker_data)
#     print(data)
#     file_name = f"CSV/{ticker}.csv"
#     data.to_csv(file_name)

# tickers = pd.read_csv('CSV/symbol.csv', header=None)[1].tolist()
# tickers.pop(0)
# stocks = (
#     (pd.concat(
#         [pd.read_csv(f"CSV/{ticker}.csv", index_col='Date', parse_dates=True)[
#             'Close'
#         ].rename(ticker) for ticker in tickers],
#         axis=1,
#         sort = True
#     ))
# )
# stocks = stocks.loc[:,~stocks.columns.duplicated()]

# def momentum(Closes):
#     returns = np.log(Closes)
#     x = np.arange(len(returns))
#     slope, _, rvalue, _, _ = linregress(x, returns)
#     return ((1 + slope) **252) * (rvalue **2)

# momentums = stocks.copy(deep=True)
# momentums = momentums.dropna()
# print(momentums)
# for ticker in tickers:
#     momentums[ticker] = stocks[ticker].rolling(90).apply(momentum,raw=False)

# plt.figure(figsize=(12,9))
# plt.xlabel('Days')
# plt.ylabel('Stock Price')

# bests = momentums.max().sort_values(ascending=False).index[:5]
# print(bests)
# for best in bests:
#     end = momentums[best].index.get_loc(momentums[best].idxmax())
#     rets = np.log(stocks[best].iloc[end - 90:end])
#     x = np.arange(len(rets))
#     slope, intercept , r_value, p_value , std_err = linregress(x, rets)
#     plt.plot(np.arange(180),stocks[best][end-90:end+90])
#     plt.plot(x, np.e ** (intercept + slope * x))
#     plt.show()
