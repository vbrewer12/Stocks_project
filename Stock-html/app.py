from flask import Flask, render_template, jsonify, request
import sqlite3
import os
from functools import wraps
import json
import pandas as pd
import numpy as np
import plotly.express as px

# make sure to pip install plotly.express-- "pip install plotly-express"

app = Flask(__name__)

# Database helper functions
def get_db_connection():
    """Create a database connection and return the connection object"""
    conn = sqlite3.connect('Stocks_data.sqlite')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def query_db(query, args=(), one=False):
    """Query the database and return results as dictionaries"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, args)
        rv = [dict(row) for row in cur.fetchall()]
        conn.commit()
        return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()

 # Routes

@app.route("/")
def index():
    """Render the main dashboard page"""
    df3 = pd.read_csv("data/percent_change.csv")

    df_numeric = df3.select_dtypes(include='number')
    df_rolled = df_numeric.rolling(90).mean()

    df3 = pd.concat([df3["Date"], df_rolled], axis=1)
    df3['Date'] = pd.to_datetime(df3['Date'])


    selected_tickers = ['BA', 'LUV', 'CL=F', 'XOP', 'XME', 'HMC', 'GM', 'PFE','GC=F','XLF',
    'SPY','^FVX','FSPTX']


    df_selected = df3[['Date'] + selected_tickers]

    df_long = df_selected.melt(id_vars='Date', var_name='Ticker', value_name='Percent Change')


    fig = px.line(df_long, x='Date', y='Percent Change', color='Ticker', title='Percent Change for Selected Tickers, 90 Day Rolling Mean' , height=900)

    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Percent Change')
    # Export to HTML file
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template("index.html",graph=graph_html)


@app.route("/info.html")
def info():
    # the info page
    stock_info = pd.read_csv("data/stock_info.csv")
    stock_html = stock_info.to_html()
    print(stock_info)

    return render_template("info.html", table = stock_html)


@app.route("/api/stockprices")
def get_stock_prices():
    ticker =  request.args.get('selectedTicker')
   

    query = f"""
        SELECT {ticker}
        FROM Price
        WHERE  strftime('%Y-%m-%d', Date) BETWEEN ? AND ?;
        """
    start_date= '2024-01-03'
    end_date= '2025-04-10'
    args = (start_date, end_date)

    stock_price = query_db(query,args)
    return jsonify(stock_price)

if __name__ == "__main__":
    # Enable debug mode in development environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=True)