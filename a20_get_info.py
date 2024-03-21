import pandas as pd
import json
from datetime import datetime
import yfinance as yf
import os

def load_info(symbols, data_path):
    """Download info data for the ticker and save as JSON."""
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    for symbol in symbols:
        ticker_data = yf.Ticker(symbol)
        info_data = ticker_data.info
        df = pd.DataFrame([info_data])
        df.to_json(f"{data_path}/{symbol}.json", orient='records', lines=True, force_ascii=False, indent=4)

def get_json_values(symbols, data_path):
    market_caps = []
    for symbol in symbols:
        json_file_path = f'{data_path}/{symbol}.json'
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
            # Directly access 'marketCap' from the dictionary without indexing
            market_cap = json_data.get('marketCap')
            if market_cap:
                market_caps.append([symbol, market_cap])
        else:
            print(f'File not found: {json_file_path}')

    df = pd.DataFrame(market_caps, columns=['Symbol', 'MarketCap']).sort_values(by='MarketCap', ascending=False).reset_index(drop=True)
    return df



def main():
    data_path = 'data/info'
    symbols_path = 'data/tickers/symbols_all.csv'
    symbols_all = pd.read_csv(symbols_path)['Symbol'].tolist()
    symbols = symbols_all  # For testing with a subset

    load_info(symbols, data_path)
    df = get_json_values(symbols, data_path)
    df.to_csv('data/tickers/symbols_mktcap.csv')
    print(df)

if __name__ == "__main__":
    main()

