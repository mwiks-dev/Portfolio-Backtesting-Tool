import pandas as pd
import datetime as dt
import yfinance as yf
from pandas.tseries.offsets import MonthEnd
from sqlalchemy import create_engine


data = pd.read_csv('https://www1.nseindia.com/content/indices/ind_nifty50list.csv',header=None)[2].tolist()
data.pop(0)
tickers = data
# print(tickers)
tickerdata = []

for symbol in tickers:
    symbol+='.NS'
    print(symbol)
    tickerdata.append(yf.download(symbol,start='2017-01-01', end='2018-01-01').reset_index())
    # print(tickerdata)

engine = create_engine('postgresql://mwiks-dev:1455@localhost/nsedb')

for frame,symbol in zip(tickerdata,tickers):
    frame.to_csv('CSV/'+symbol+'.csv')

for frame,symbol in zip(tickerdata,tickers):
    frame.to_sql(symbol, engine, if_exists='replace', index=False)
    print(symbol+' done')

# df = pd.concat(tickerdata)
# print(df)

# pd.set_option('display.max_columns',185)
# pd.set_option('display.max_rows',125)


# df = df.groupby("Date")
# df = df.set_index("Date")

# # df.dropna(axis=1)
# df.to_csv('CSV/Tickerdata.csv')
# # print(df)


# mtlprices  = df.resample('M').last()
# print(mtlprices)

# formation = dt.datetime(2019,1,1)

# begin_measurement = formation - MonthEnd(12)
# b_time = begin_measurement.strftime('%Y-%m-%d')
# # print(b_time)
# end_measurement = formation - MonthEnd(1)
# e_time = end_measurement.strftime('%Y-%m-%d')
# # print(e_time)

# price_end = mtlprices.loc[e_time]
# # print(price_end)

# price_begin = mtlprices.loc[b_time]
# # print(price_begin)

# pct_return_12 = (price_end - price_begin) / price_begin * 100
# print(pct_return_12.dropna())

# # winners = ret_12_1.nlargest(3)
# # print(winners)

# # winnerret = mtlprices.loc[formation + MonthEnd(1), winners.index]/mtlprices.loc[formation, winners.index] - 1
# # print(winnerret)

# # momentum_profit = winnerret.mean()
# # print(momentum_profit)

# # def momentumprofit(formation, holdingperiod=1):
# #     begin_measurement = formation - MonthEnd(12)
# #     end_measurement = formation - MonthEnd(1)
# #     price_end = mtlprices.loc[end_measurement]
# #     price_begin = mtlprices.loc[begin_measurement]
# #     ret_12 = price_end /price_begin - 1
# #     winners = ret_12.nlargest(3)
# #     winnerret = mtlprices.loc[formation + MonthEnd(holdingperiod), winners.index]/mtlprices.loc[formation, winners.index] - 1
# #     momentum_profit = winnerret.mean()
# #     return momentum_profit

# # formation = dt.datetime(2019,1,1)

# # momentumprofit(formation)
# # print(momentumprofit(formation))

# # mtlprices.index

# # profits , dates , holding = [],[],[]
# # for i in (1,3,6):
# #     for j in mtlprices.index[12:-i]:
# #         profits.append(momentumprofit(j, holdingperiod=i))
# #         dates.append(j + MonthEnd(i))
# #         holding.append(i)

# # frame = pd.DataFrame({'Momentumprofit':profits,'Holdingperiod':holding},index = dates)
# # frame.groupby('holdingperiod').mean()
