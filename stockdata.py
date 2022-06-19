#S&P 500 Stock Tickers only

import requests
import json
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import sqlite3

#RVTLZQGNNKI1AZW7
#sgSC_ueaKrkbwOLrKud2LVF_JFovm6Eo

# Set the start and end date
start_date = '1990-01-01'
end_date = '2021-07-12'

tickers_list = ['AAPL', 'IBM', 'MSFT', 'WMT']

# Create placeholder for data
data = pd.DataFrame(columns=tickers_list)

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
#fetching the data from the above loc
print(tickers.head())


# Fetch the data in the array trackers list:
for ticker in tickers_list:
    data[ticker] = yf.download(ticker, start_date, end_date)['Adj Close']
'''   
# Print first 5 rows of the data
print(data)
'''
# Fetch the data
#the tickers['symbol'] are the tickers, so i need to pass them as the argument so how should i do it

'''
for ticker in tickers['Symbol']:
    data[ticker] = yf.download(ticker, start_date, end_date)['Adj Close']
'''

    
# data.plot(figsize=(10, 7))
'''
# Show the legend
plt.legend()

# Define the label for the title of the figure
plt.title("Adjusted Close Price", fontsize=16)

# Define the labels for x-axis and y-axis
plt.ylabel('Price', fontsize=14)
plt.xlabel('Year', fontsize=14)

# Plot the grid lines
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()
'''

#   html = tickers.head().to_html()
#   text_file = open("stocktable.html", "w")
#   text_file.write(html)
#   text_file.close()
# backtest inputs
bt_inputs = {'tickers': ['BA', 'UNH', 'MCD', 'HD'],
'start_date': '2019-01-01',
'end_date': '2021-06-01'}

# create a sql connection
con = sqlite3.connect('stock.db')
c = con.cursor()


# create price table
query1 = """CREATE TABLE IF NOT EXISTS prices (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
price REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query1.replace('\n',' '))


# create volume table
query2 = """CREATE TABLE IF NOT EXISTS volume (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
volume REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query2.replace('\n',' '))

#until here only the tables are created now the data will be fetched for the thing
def download(bt_inputs, proxy = None):
    data = yf.download(tickers= bt_inputs['tickers'],
                       start = bt_inputs['start_date'],   
                       end = bt_inputs['end_date'],
                       interval = '1d',
                       prepost = True,
                       threads = True,
                       proxy = proxy)
    return data

test = download(bt_inputs)
adj_close = test['Adj Close']
volume = test['Volume']

# convert wide to long
adj_close_long = pd.melt(adj_close.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name ="ticker", value_name="price")
volume_long = pd.melt(volume.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "volume")

#adding the data in the sql table
adj_close_long.to_sql('prices', con, if_exists='append', index=False)
volume_long.to_sql('volume', con, if_exists='append', index=False)

'''
# inputs
select_tickers = bt_inputs['tickers']
start_date = bt_inputs['start_date']
end_date = bt_inputs['end_date']
# construct query
query = """
select * from prices
where ticker in ('"""+ "','".join(select_tickers) + """')
and Date >= '"""+ start_date + """'
and Date < '""" + end_date + "'"
c.execute(query.replace('\n',' '))
result = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'price'])
# convert to datetime
result['Date'] = pd.to_datetime(result['Date'])
'''