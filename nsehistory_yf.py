import math
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
import matplotlib.pyplot as plt



data = pd.read_csv('https://www1.nseindia.com/content/indices/ind_nifty50list.csv',header=None)[2]
data.pop(0)
tickers = data
# print(tickers)
tickerdata = []

for symbol in tickers:
    symbol+='.NS'
    # print(symbol)
    #Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    tickerdata.append(yf.download(symbol,start='2017-01-01', end='2019-05-01').reset_index())
    # print(tickerdata)

engine = create_engine('postgresql://mwiks-dev:1455@localhost/nsedb')

for frame,symbol in zip(tickerdata,tickers):
    frame.to_csv('CSV/'+symbol+'.csv')

for frame,symbol in zip(tickerdata,tickers):
    frame.to_sql(symbol, engine, if_exists='replace', index=False)

df = pd.DataFrame() 
for name in tickers:
    df = df.append(pd.read_sql(f'SELECT "Date","Open","Adj Close" AS "{name}" FROM "{name}"', engine))
pd.set_option('display.max_columns', 185)
df = df.set_index(pd.DatetimeIndex(df['Date'].values))

df.drop(['Date','Open'], axis=1, inplace=True)
# print(df)

mtlprices  = df.resample('M').last()
pre_mtlprices = df.resample('M').first()

monthly_returns = mtlprices - pre_mtlprices
# print(monthly_returns)
annual_returns = monthly_returns.mean() * 12
annual_pct_returns = annual_returns.pct_change()
# print(annual_pct_returns)
# print(annual_returns)

annual_risks = monthly_returns.std() * math.sqrt(12)
# print(annual_risks)

sorted_annual_returns = annual_returns.sort_values(ascending=False)
# print(sorted_annual_returns)

plt.bar(sorted_annual_returns.index, sorted_annual_returns.values)
plt.ylabel('Annual Returns')
plt.xlabel('Assets')
plt.xticks(rotation=90)
plt.title('Annual Returns of NSE Assets')
plt.show()

df2 = pd.DataFrame()
df2['Expected Annual Returns'] = annual_returns
df2['Expected Annual Risks'] = annual_risks
df2['Company Tickers'] = df2.index
df2['Ratio'] = df2['Expected Annual Returns']/df2['Expected Annual Risks']
df2.sort_values(by='Ratio',axis=0,inplace=False,ascending=False)
df2.to_csv('CSV/winners.csv')
# print(df2)

fig, ax = plt.subplots(figsize=(15,10))
plt.title('Expected Annual Returns of NSE Assets vs Expected Annual Risk')
ax.scatter(df2['Expected Annual Risks'], df2['Expected Annual Returns'], c ='red')
ax.set_xlabel('Expected Annual Risks')
ax.set_ylabel('Expected Annual Returns')

for idx, row in df2.iterrows():
    ax.annotate(row['Company Tickers'], (row['Expected Annual Risks'], row['Expected Annual Returns']), c='green')

plt.show()

assets = df.columns

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
 
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()

cleaned_weights = ef.clean_weights()
# print(cleaned_weights)

ef.portfolio_performance(verbose=True)
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

portfolio_val = 10000
latest_prices = get_latest_prices(df)
weights = cleaned_weights 
da = DiscreteAllocation(weights, latest_prices,total_portfolio_value= portfolio_val)

allocation , leftover = da.lp_portfolio()
# print("Discrete allocation:", allocation)
# print("Funds:rupees", leftover)

change_asset_list = []
for ticker in df2['Company Tickers'].values:
    better_assets = df2.loc[(df2['Expected Annual Returns'] > df2['Expected Annual Returns'][ticker]) & (df2['Expected Annual Risks'] < df2['Expected Annual Risks'][ticker])].empty
    if better_assets == False:
        change_asset_list.append(ticker)
df2.drop(change_asset_list, inplace=True)
print(df2)
        

