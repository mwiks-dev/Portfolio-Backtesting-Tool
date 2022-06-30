import yfinance as yf
import pandas as pd
import datetime as dt
import pandas_datareader.data as web

# nse = yf.Ticker('^NSEBANK')
print("Enter valid SYMBOL")
nse = yf.Ticker(input(''))
print("Enter start date in YYYY-MM-DD format")
s_time = dt.datetime.strptime(input(''), '%Y-%m-%d')
print("Enter end date in YYYY-MM-DD format")
e_time = dt.datetime.strptime(input(''), '%Y-%m-%d')

# print("Enter interval in minutes,days,weeks or months")
# print('For example if you want to get data for last 30 minutes, enter "30m"')
# print('For example if you want to get data for last 5 days, enter "5d"')
# print('For example if you want to get data for last 2 weeks, enter "2w"')
# print('For example if you want to get data for last 1 month, enter "1mo"')
# interval = input('')

# nse_history = nse.history(period='max')
# nse_history = nse.history(start='2022-05-01', end='2022-05-31',interval="30m",actions=False)
nse_history = nse.history(start=s_time, end= e_time,actions=False,prepost=True)

pd.options.display.width = 0
pd.set_option('display.max_rows',20000)
pd.set_option('display.max_columns',4)
print(nse_history)

nse_history.to_csv('output.csv')

