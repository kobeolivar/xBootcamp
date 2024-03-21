import pandas as pd
import json
from datetime import datetime
import yfinance as yf
import tqdm
from icecream import ic 



def load_info(symbols, data_path):       
        """Download info data for the ticker and save as JSON."""
        for symbol in symbols:
            ticker_data = yf.Ticker(symbol)
            info_data = ticker_data.info
            df = pd.DataFrame([info_data])
            df.to_json(f"{data_path}/{symbol}.json", orient='records', lines=False, force_ascii=False, indent=4)

        # ticker_data = yf.Ticker(symbol)
        # info_data = ticker_data.info
        # df = pd.DataFrame([info_data])
        # df.to_json(f"{datapath}/{symbols}.info", orient='records', lines=True)

        



def get_json_values(symbols, data_path):
    # Initialize an empty list to collect [symbol, marketCap] pairs
    market_caps = []

    
    for symbol in symbols:
        # Construct the file path
        json_file_path = f'{data_path}/{symbol}.json'
      
        try:
            # Read the JSON file
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
            print(json_file_path)

            # Extract the marketCap value
            market_cap = get_marketCap(symbol,market_caps)
            ic(market_cap)
            exit()

            # Check if marketCap was found and add to the data list
            if market_cap is not None:
                market_caps.append([symbol, market_cap])
        except FileNotFoundError:
            print(f'File not found: {json_file_path}')
        except json.JSONDecodeError:
            print(f'Error decoding JSON from file: {json_file_path}')
    
    # Create a DataFrame from the collected data
    df = pd.DataFrame(market_caps, columns=['Symbol', 'MarketCap'])
    df_sorted = df.sort_values(by='MarketCap', ascending=False)
    
    # Resetting the index of the sorted DataFrame
    df_sorted_reset = df_sorted.reset_index(drop=True)

    df_sorted_reset.to_csv(f'data/tickers/symbols_mktcap.csv') 
    return df_sorted_reset

def get_marketCap(symbol, market_caps):
    with open(f'{symbol}.json', 'r') as file:
        json_data = json.load(file)

    # Check if json_data is a list
    if isinstance(json_data, list):
        # Iterate over each item (which should be a dictionary) in the list
        for item in json_data:
            # Use .get() to safely extract the 'marketCap' value
            # This will return None if 'marketCap' is not found
            market_cap = item.get('marketCap', None)
            # If you want to change 'marketCap' to 'mar_cap' in each dictionary:
            if 'marketCap' in item:
                item['mar_cap'] = item.pop('marketCap')
            # Append the marketCap value (or None) to the list
            market_caps.append(market_cap)
    else:
        # Handle the case where json_data is not a list (e.g., a single dictionary)
        market_cap = json_data.get('marketCap', None)
        market_caps.append(market_cap)

def main():
    symbols_path = f'data/tickers/symbols_all.csv'
    symbols_all = pd.read_csv(symbols_path)['Symbol'].tolist()
    symbols = symbols_all[:5]
    data_path = 'data/info'
    df = load_info(symbols, data_path)
    print('load_info',df)
    df = get_json_values(symbols, data_path)
    print(df)        

main()
#data/info/BEN.json