import yfinance as yf
import pandas as pd
import datetime
import pandas_datareader.data as web
import csv
import collections

#the start expression is for February 1, 2021
start = datetime.date(2021,2,1)
 
#the end expression is for February 28, 2019
end = datetime.date(2021,2,28)

nse = yf.Ticker('^NSEI')

# nse_history = nse.history(period='max')
# nse_history = nse.history(start='2022-05-01', end='2022-05-31',interval="30m",actions=False)
nse_history = nse.history(start='2022-05-01', end='2022-05-31',interval="1d",actions=False,prepost=True)

pd.options.display.width = 0
pd.set_option('display.max_rows',20000)
print(nse_history)

with open('/home/mwiks-dev/Projects/Personal/Portfolio-Backtest/output.txt') as f:
    data = list(csv.reader(f))

counter = collections.defaultdict(int)
for row in data:
    counter[row[0]] += 1

writer = csv.writer(open('/home/mwiks-dev/Projects/Personal/Portfolio-Backtest/output.csv', 'w'))
for row in data:
    if counter[row[0]] >= 4:
        writer.writerow(row)



# nse_data = yf.download('NSE',start='2021-2-1',end='2021-2-28',auto_adjust=True)
# print (nse_data)

# df = yf.download('NSE TSLA',start='2021-2-1',end='2021-2-28')
# df = df.drop(['Open','High','Low','Volume','Adj Close'], axis=1)
# print (df)  
# print('For nse ticket info lines')
# print(nse.info)
# print('For nse ticket info lines')
# print(nse.actions)


