from nsehistory_yf import df,tickers
import datetime as dt
from pandas.tseries.offsets import MonthEnd
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine


mtlprices  = df.resample('M').last()

formation = dt.datetime(2019,1,1)
f_time = formation.strftime('%Y-%m-%d')
# print(f_time)

begin_measurement = formation - MonthEnd(12)
b_time = begin_measurement.strftime('%Y-%m-%d')
# print(b_time)
end_measurement = formation - MonthEnd(1)
e_time = end_measurement.strftime('%Y-%m-%d')
# print(e_time)

price_end = mtlprices.loc[e_time]
# print(price_end)

price_begin = mtlprices.loc[b_time]
# print(price_begin)

pct_return_12 = (price_end - price_begin) / price_begin * 100
# # print(pct_return_12.dropna())

winners = pct_return_12.nlargest(10)
winners.to_csv('winners.csv')
# print(winners)

w_symbols = pd.read_csv('winners.csv',header=None)[0]
w_symbols.pop(0)
# print(w_symbols)
winner_data = []

for symbol in w_symbols:
    symbol+='.NS'
    # print(symbol)
    #Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    winner_data.append(yf.download(symbol,start='2017-01-01', end='2019-05-01').reset_index())
# print(winner_data)

engine = create_engine('postgresql://mwiks-dev:1455@localhost/nsedb')

for frame,symbol in zip(winner_data,w_symbols):
    frame.to_sql(symbol, engine, if_exists='replace', index=False)

df3 = pd.DataFrame()
df5 = pd.DataFrame()

for index in w_symbols:
    df3 = df3.append(pd.read_sql(f'SELECT "Date","Open","Adj Close" AS "{index}" FROM "{index}"', engine))
    df5 = df5.append(pd.read_sql(f'SELECT "Date","Open","Adj Close" AS "{index}" FROM "{index}"', engine))
pd.set_option('display.max_columns', 185)
df3 = df3.set_index(pd.DatetimeIndex(df3['Date'].values))
df5 = df5.set_index(pd.DatetimeIndex(df5['Date'].values))


df3.drop(['Date','Open'], axis=1, inplace=True)
df5.drop(['Date','Open'], axis=1, inplace=True)
# print(df5)

w_mtlprices = df5.resample('M').last()
w_pre_mtlprices = df5.resample('M').first()

w_monthly_returns = w_mtlprices - w_pre_mtlprices
w_annual_returns = w_monthly_returns.mean() * 12

w_annual_risks = w_monthly_returns.std() * 12

sorted_winner_returns = w_annual_returns.sort_values(ascending=False)

df5 = pd.DataFrame()
df5['Expected Annual Returns'] = w_annual_returns
df5['Expected Annual Risks'] = w_annual_risks
df5['Company Tickers'] = df5.index
df5['Ratio'] = df5['Expected Annual Returns']/df5['Expected Annual Risks']
df5.sort_values(by='Ratio',axis=0,inplace=False,ascending=False)
df5.to_csv('winner_returns.csv')
# print(df5)
winner_assets = df3.columns

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
 
mu = expected_returns.mean_historical_return(df3)
S = risk_models.sample_cov(df3)

ef2 = EfficientFrontier(mu, S)
weights = ef2.max_sharpe()

cleaned_weights = ef2.clean_weights()
# print(cleaned_weights)

ef2.portfolio_performance(verbose=True)
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

portfolio_val = 10000
latest_prices = get_latest_prices(df3)
weights = cleaned_weights 
da = DiscreteAllocation(weights, latest_prices,total_portfolio_value= portfolio_val)

allocation , leftover = da.lp_portfolio()
# print("Discrete allocation:", allocation)
# print("Funds:rupees", leftover)

winner_change_list = []
for ticker in df5['Company Tickers'].values:
    better_winners = df5.loc[(df5['Expected Annual Returns'] > df5['Expected Annual Returns'][ticker]) & (df5['Expected Annual Risks'] < df5['Expected Annual Risks'][ticker])].empty
    if better_winners == False:
        winner_change_list.append(ticker)
# print(winner_change_list)
df5.drop(winner_change_list, inplace=True)
print(df3)
print('Enter start date in yyyy-mm-dd')
s_date = dt.datetime.strptime(input(''), '%Y-%m-%d')
print('Enter end date in yyyy-mm-dd')
e_date = dt.datetime.strptime(input(''), '%Y-%m-%d')
details = []
for symbol in df5:
    details.append(yf.download(symbol,start=s_date, end=e_date).reset_index())
print(details)


