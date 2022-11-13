import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt



# data = pd.read_csv('https://www1.nseindia.com/content/indices/ind_nifty50list.csv',header=None)[2]
# data.pop(0)
# tickers = data
# # print(tickers)
# tickerdata = []
# for symbol in tickers:
#     symbol+='.NS'
#     # print(symbol)
#     #Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
#     tickerdata.append(yf.download(symbol,start='2017-01-01', end='2019-05-01'))
#     # print(tickerdata)

# for frame,symbol in zip(tickerdata,tickers):
#     frame.to_csv('CSV/'+symbol+'.csv')

# assign path
path, dirs, files = next(os.walk("CSV/"))
file_count = len(files)

df = pd.DataFrame() 
# append datasets to the list
for i in range(file_count):
    df = df.append(pd.read_csv("CSV/"+files[i]))
    
# df = df.set_index(pd.DatetimeIndex(df['Date'].values))
# df.drop(['Date','Open','Close','High','Low','Volume'], axis=1, inplace=True)
print(df)
# # ranking = df.loc['2017-12-31':'2018-12-31']

# end_mtlprices  = df.resample('M').last()
# # print(mtlprices)
# start_mtlprices = df.resample('M').first()
# # print(start_mtlprices)
# monthly_returns = end_mtlprices - start_mtlprices
# # print(monthly_returns)
# annual_returns = monthly_returns.mean()*12
# # print(annual_returns)
# annual_pct_returns = annual_returns.pct_change()
# # print(annual_pct_returns)

# sorted_annual_returns = annual_pct_returns.sort_values(ascending=False)
# print(sorted_annual_returns)

# plt.bar(sorted_annual_returns.index, sorted_annual_returns.values)
# plt.ylabel('Annual Returns')
# plt.xlabel('Assets')
# plt.xticks(rotation=90)
# plt.title('Annual Returns of NSE Assets')
# plt.show()