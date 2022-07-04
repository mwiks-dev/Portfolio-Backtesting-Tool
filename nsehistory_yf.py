from click import style
import matplotlib as mpl
import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# nse = yf.Ticker('^NSEBANK')
print("Enter valid SYMBOL")
nse = yf.Ticker(input(''))
print("Enter start date in YYYY-MM-DD format")
s_time = dt.datetime.strptime(input(''), '%Y-%m-%d')
print("Enter end date in YYYY-MM-DD format")
e_time = dt.datetime.strptime(input(''), '%Y-%m-%d')
# nse_history = nse.history(period='max')
nse_history = nse.history(start=s_time, end= e_time,actions=False,prepost=True)

pd.options.display.width = 0
pd.set_option('display.max_rows',20000)
pd.set_option('display.max_columns',6)

nse_history['Price Change'] = nse_history['Close'].rolling(window=30).mean()
nse_history['Volume Change'] = nse_history['Volume'].rolling(window=30).mean()
nse_history = nse_history[nse_history['Price Change'].notna()]
nse_history.to_csv('output.csv')
# tickers = pd.read_csv('output.csv')
parse_dates = ['Date_column']
tickers = pd.read_csv('output.csv', parse_dates=['Date'])
tickers.head()
print(tickers.head())
print(tickers.info())

fig, ax = plt.subplots(figsize=(10,10))

# ax.plot(tickers['Date'], tickers['Price Change'], color='red')
# ax.set(xlabel='Date', ylabel='Price Change',title='NSE Price Change')
# plt.show()

# close = nse_history['Close']
# pplot = nse_history['Price Change']
# vplot = nse_history['Volume Change']

# mpl.rc('figure', figsize=(15,10))
# # style.use('ggplot')

# # plt.plot(pplot,vplot)
# # plt.show()


# # close.plot(label=stock,legend=True)
# pplot.plot(label='Price Change 30d',legend=True , marker="*")
# vplot.plot(secondary_y = True, label='Volume Change 30d',legend=True,marker='*')
# plt.plot(pplot,vplot)
# plt.show()

# print(tickers)
# stocksH = (
#     pd.concat(
#         [pd.read_csv(f"output.csv", index_col='Date',parse_dates=True)[
#             'Close'
#         ].rename(ticker)
#         for ticker in tickers],
#         axis=1,
#         sort=True
#     )
# )
# stocks = stocksH.loc[:,~stocksH.columns.duplicated()]
# print(stocks)
# def momentum():
#     returns = np.log()
#     x = np.arange(len(returns))
#     slope, _, rvalue, _, _ = linregress(x, returns)
#     return ((1 + slope) ** 252) * (rvalue ** 2)

# momentums = stocks.copy(deep=True)
# for ticker in tickers:
#     momentums[ticker] = stocks[ticker].rolling(90).apply(momentum, raw=False)

# df = momentums.dropna()
# # print(df)
# # plt.figure(figsize=(12,9))
# # plt.xlabel('Days')
# # plt.ylabel('Stock Price')

# # bests = momentums.max().sort_values(ascending=False).index[:5]
# # for best in bests:
# #     end = momentums[best].index.get_loc(momentums[best])
# #     rets = np.log(stocks[best].iloc[end - 90:end])
# #     x = np.arange(len(rets))
# #     slope, intercept , r_value , p_value , std_err = linregress(x, rets)
# #     plt.plot(np.arange(180), stocks[best][end-90:end+90])
# #     plt.plot(x,np.e ** (intercept + slope * x))