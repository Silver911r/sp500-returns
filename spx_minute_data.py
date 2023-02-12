import requests
import pandas as pd
import sqlite3
import datetime
import time
import logging

logging.basicConfig(filename="spx.log", level=logging.INFO)

# Define the API key and the symbol for SPX
api_key = ''

# convert unix timestamp
def convert_timestamp(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return dt

def is_market_open():
    response = requests.get('https://api.tradier.com/v1/markets/clock',
    params={'delayed': 'true'},
    headers={'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
    )
    data = response.json()
    if 'closed' == data['clock']['state']:
        return False
    elif 'open' == data['clock']['state']:
        return True


def retrieve_quote():
    logging.info("Retrieve Quote")
    response = requests.get('https://api.tradier.com/v1/markets/quotes',
    params={'symbols': 'SPX', 'greeks': 'false'},
    headers={'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
    )
    return response.json()

def convert_and_format_dataframe(data):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame([data['quotes']['quote']])
    df['trade_date'] = pd.to_datetime(convert_timestamp(df['trade_date'][0]))
    df['bid_date'] = pd.to_datetime(convert_timestamp(df['bid_date'][0]))
    df['ask_date'] = pd.to_datetime(convert_timestamp(df['ask_date'][0]))
    df.set_index(df['trade_date'],inplace=True)
    # Remove the original "date" column
    df.drop("trade_date", axis=1, inplace=True)
    return df

def save_to_sqlite(df):
    # Connect to the SQLite database
    conn = sqlite3.connect("spx.db")
    # Store the SPX data in the SQLite database
    df.to_sql("spx", conn, if_exists="append")
    # Close the connection to the database
    conn.close()

def collect_spx_data():
    try:
        if is_market_open():
            data = retrieve_quote()
            df = convert_and_format_dataframe(data)
            save_to_sqlite(df)
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)
        
def main():
    while True:
        collect_spx_data()
        time.sleep(60)

if __name__ == "__main__":
    main()
