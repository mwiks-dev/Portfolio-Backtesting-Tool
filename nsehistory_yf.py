import math
import pandas as pd
import datetime as dt
import yfinance as yf
from pandas.tseries.offsets import MonthEnd
from sqlalchemy import create_engine
import numpy as np
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
    # print(symbol+' done')

df = pd.DataFrame()
    
for name in tickers:
    df = df.append(pd.read_sql(f'SELECT "Date","Open","Adj Close" AS "{name}" FROM "{name}"', engine))
pd.set_option('display.max_columns', 185)
df = df.set_index(pd.DatetimeIndex(df['Date'].values))

df.drop(['Date','Open'], axis=1, inplace=True)
# print(df)

mtlprices  = df.resample('M').last()
pre_mtlprices = df.resample('M').first()
# print(mtlprices)
monthly_returns = mtlprices - pre_mtlprices
# print(monthly_returns)
annual_returns = monthly_returns.mean() * 12
print(annual_returns)

annual_risks = monthly_returns.std() * math.sqrt(12)
print(annual_risks)
# # daily_returns = df.pct_change(1)
# # print(daily_returns)

# annual_returns = daily_returns.mean() * 252
# # print(annual_returns)

# annual_risks = daily_returns.std() * math.sqrt(252)
# # print(annual_risks)

# sorted_annual_returns = annual_returns.sort_values(ascending=False)
# # print(sorted_annual_returns)

# plt.bar(sorted_annual_returns.index, sorted_annual_returns.values)
# plt.ylabel('Annual Returns')
# plt.xlabel('Assets')
# plt.xticks(rotation=90)
# plt.title('Annual Returns of NSE Assets')
# # plt.show()

# df2 = pd.DataFrame()
# df2['Expected Annual Returns'] = annual_returns
# df2['Expected Annual Risk'] = annual_risks
# df2['Company Tickers'] = df2.index
# df2['Ratio'] = df2['Expected Annual Returns']/df2['Expected Annual Risk']
# df2.sort_values(by='Ratio',axis=0,inplace=False,ascending=False)
# df.to_csv('CSV/ratios.csv')
# print(df2.nlargest(10,'Ratio'))

# fig, ax = plt.subplots(figsize=(15,10))
# plt.title('Expected Annual Returns of NSE Assets vs Expected Annual Risk')
# ax.scatter(df2['Expected Annual Risk'], df2['Expected Annual Returns'], c ='DarkBlue')
# ax.set_xlabel('Expected Annual Risk')
# ax.set_ylabel('Expected Annual Returns')

# for idx, row in df2.iterrows():
#     ax.annotate(row['Company Tickers'], (row['Expected Annual Risk'], row['Expected Annual Returns']), c='green')

# plt.show()



# assets = df.columns

# from pypfopt.efficient_frontier import EfficientFrontier
# from pypfopt import risk_models
# from pypfopt import expected_returns
 
# mu = expected_returns.mean_historical_return(df)
# S = risk_models.sample_cov(df)

# ef = EfficientFrontier(mu, S)
# weights = ef.max_sharpe()

# cleaned_weights = ef.clean_weights()
# print(cleaned_weights)

# ef.portfolio_performance(verbose=True)

# from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# portfolio_val = 10000
# latest_prices = get_latest_prices(df)
# weights = cleaned_weights 
# da = DiscreteAllocation(weights, latest_prices,total_portfolio_value= portfolio_val)

# allocation , leftover = da.lp_portfolio()
# print("Discrete allocation:", allocation)
# print("Funds:rupees", leftover)

# def get_company(symbol):
#     url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+symbol+'&region=1=&lang=en'
#     result = requests.get(url).json()
#     for x in result['ResultSet']['Result']:
#         if x['symbol'] == symbol:
#             return x['name']

# company_name = []
# for symbol in allocation:
#     company_name.append(get_company(symbol))
# print(company_name)

# discrete_allocation_list = []
# for symbol in allocation:
#     discrete_allocation_list.append(allocation.get(symbol))


# portfolio_df = pd.DataFrame(columns = ['Company_Ticker','Discrete_val_'+str(portfolio_val)])

# portfolio_df['Company_Ticker'] = allocation
# portfolio_df['Discrete_val_'+str(portfolio_val)] = discrete_allocation_list
# portfolio_df.to_csv('CSV/Potfolio.csv')
# print(portfolio_df)

# mtlprices  = df.resample('M').last()
# # # print(mtlprices)

# formation = dt.datetime(2019,1,1)
# f_time = formation.strftime('%Y-%m-%d')
# # # print(f_time)

# begin_measurement = formation - MonthEnd(12)
# b_time = begin_measurement.strftime('%Y-%m-%d')
# # # print(b_time)
# end_measurement = formation - MonthEnd(1)
# e_time = end_measurement.strftime('%Y-%m-%d')
# # print(e_time)

# price_end = mtlprices.loc[e_time]
# # # print(price_end)

# price_begin = mtlprices.loc[b_time]
# # # print(price_begin)

# pct_return_12 = (price_end - price_begin) / price_begin * 100
# # # print(pct_return_12.dropna())

# winners = pct_return_12.nlargest(50)
# winners.to_csv('CSV/winners.csv')
# # print(winners)


# # # i)Create portfolio with the top 10
# # # ii)Fund value , no of stocks held, value when buying
