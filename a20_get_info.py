import pandas as pd
import json
from datetime import datetime
import yfinance as yf
import tqdm



def load_info(symbols, datapath):       
        """Download info data for the ticker and save as JSON."""
        for symbol in symbols:
            ticker_data = yf.Ticker(symbol)
            info_data = ticker_data.info
            df = pd.DataFrame([info_data])
            df.to_json(f"{datapath}/{symbol}.json", orient='records', lines=True)

        # ticker_data = yf.Ticker(symbols)
        # info_data = ticker_data.info
        # df = pd.DataFrame([info_data])
        # df.to_json(f"{datapath}/{symbols}.info", orient='records', lines=True)

        



def get_json_values(symbols, data_path):
    # Initialize an empty list to collect [symbol, marketCap] pairs
    data = []

    
    for symbol in symbols:
        # Construct the file path
        json_file_path = f'{data_path}/{symbol}.json'
        try:
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
            
            # Extract the marketCap value
            market_cap = json_data.get('marketCap', None)
            
            # Check if marketCap was found and add to the data list
            if market_cap is not None:
                data.append([symbol, market_cap])
        except FileNotFoundError:
            print(f'File not found: {json_file_path}')
        except json.JSONDecodeError:
            print(f'Error decoding JSON from file: {json_file_path}')
    
    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=['Symbol', 'MarketCap'])
    df_sorted = df.sort_values(by='MarketCap', ascending=False)
    
    # Resetting the index of the sorted DataFrame
    df_sorted_reset = df_sorted.reset_index(drop=True)

    df_sorted_reset.to_csv(f'data/tickers/symbols_mktcap.csv') 
    return df_sorted_reset

def main():
    symbols_path = f'/home/larry/atapps/aStockTrading/data/tickers/symbols_all.csv'
    symbols = pd.read_csv(symbols_path)['Symbol'].tolist()
    data_path = '/home/larry/atapps/aStockTrading/data/info'
    #df = load_info(symbols, data_path)
    df = get_json_values(symbols, data_path)
    print(df)        

main()
