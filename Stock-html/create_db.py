import pandas as pd
import sqlite3
# import requests

#load into DataFrame

df = pd.read_csv('data/Industries.csv')
df2 = pd.read_csv('data/percent_change.csv')
df3 = pd.read_csv('data/stock_prices.csv')

#rewrite to df to sqlite
conn = sqlite3.connect('Stocks_data.sqlite')

#write df to sqlite table
df.to_sql('Industries', conn, if_exists= "replace", index = False)
df2.to_sql('Percentage', conn, if_exists= "replace", index = False)
df3.to_sql('Price', conn, if_exists= "replace", index = False)

conn.close()


