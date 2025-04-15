from flask import Flask, render_template, jsonify, request
import sqlite3
import os
from functools import wraps
import json
import pandas as pd

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

    return render_template("index.html")


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