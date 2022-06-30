import datetime
from os import symlink
import pandas as pd
import pandas_datareader.data as web

print('Enter valid SYMBOL')
symbol = input('')
print('Enter start date in YYYY-MM-DD format')
s_time = datetime.datetime.strptime(input(''), '%Y-%m-%d')
print('Enter end date in YYYY-MM-DD format')
e_time = datetime.datetime.strptime(input(''), '%Y-%m-%d')

# date = datetime.datetime(2022, 1, 31)

# df = web.DataReader("NSE","yahoo", start, end)
df = web.DataReader(symbol,'yahoo', start=s_time, end=e_time)

pd.options.display.width = 0
df = df.drop('Adj Close', axis=1)
print(df)
df.to_csv('history.csv')


# nse = get_rbi_ref_history(start=start, end=end)
# print(nse)

# prices = get_price_list(dt=date)

# data = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]
# labels = data.loc[[124,126,127]]
# print(data.loc[[124,125,126,127]])
# allocation_pct =[.1,.2,.3,.4]

# fig = go.Figure(data=[go.Pie(labels=labels, values=allocation_pct) ])
# fig.update_layout(title_text="NSE F&O Stock List")
# fig.show()
