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

for ticker in tickers:
    tickerdata.append(yf.download(ticker, start='2022-01-01', end='2022-07-04').reset_index())

engine = create_engine('postgresql://mwiks-dev:1455@localhost/nsehistory')

for frame, symbol in zip(tickerdata, tickers):
    frame.to_csv('CSV/' + symbol + '.csv', index=False)

for frame,symbol in zip(tickerdata, tickers):
    frame.to_sql(symbol, engine, index=False)

# print(tickerdata)

# print(pd.read_sql(f'SELECT "Date" ,"Adj Close" FROM "ACC"', engine))
df = pd.DataFrame()

for name in tickers:
    df = df.append(pd.read_sql(\
        f'SELECT "Date" ,"Adj Close" AS "{name}" FROM "{name}"', engine))
pd.set_option('display.max_columns',185)

df = df.groupby("Date").sum()
df.index = pd.to_datetime(df.index)

df.to_csv('CSV/Tickerdata.csv')

mtlprices  = df.resample('M').last()
print(mtlprices)
formation = dt.datetime(2019,1,1)

begin_measurement = formation - MonthEnd(12)
end_measurement = formation - MonthEnd(1)

price_end = mtlprices.loc[end_measurement]
print(price_end)

price_begin = mtlprices.loc[begin_measurement]

ret_12_1 = price_end /price_begin - 1
print(ret_12_1)

winners = ret_12_1.nlargest(3)
print(winners)

winnerret = mtlprices.loc[formation + MonthEnd(1), winners.index]/mtlprices.loc[formation, winners.index] - 1
print(winnerret)

momentum_profit = winnerret.mean()
print(momentum_profit)

def momentumprofit(formation, holdingperiod=1):
    begin_measurement = formation - MonthEnd(12)
    end_measurement = formation - MonthEnd(1)
    price_end = mtlprices.loc[end_measurement]
    price_begin = mtlprices.loc[begin_measurement]
    ret_12 = price_end /price_begin - 1
    winners = ret_12.nlargest(3)
    winnerret = mtlprices.loc[formation + MonthEnd(holdingperiod), winners.index]/mtlprices.loc[formation, winners.index] - 1
    momentum_profit = winnerret.mean()
    return momentum_profit

formation = dt.datetime(2019,1,1)

momentumprofit(formation)
print(momentumprofit(formation))

mtlprices.index

profits , dates , holding = [],[],[]
for i in (1,3,6):
    for j in mtlprices.index[12:-i]:
        profits.append(momentumprofit(j, holdingperiod=i))
        dates.append(j + MonthEnd(i))
        holding.append(i)

frame = pd.DataFrame({'Momentumprofit':profits,'Holdingperiod':holding},index = dates)
frame.groupby('holdingperiod').mean()
print(frame)