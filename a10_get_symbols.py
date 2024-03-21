
import yfinance as yf
from yahooquery import Ticker
import pandas as pd
from icecream import ic
import requests
from bs4 import BeautifulSoup
import warnings


def get_symbolss_tickers():
        # Scrape 3 indexes from slickcharrs        
        symbolss_ndx = ['sp500','nasdaq100','dowjones']
        for ndx in symbolss_ndx:
            url= f'https://www.slickcharts.com/{ndx}'  # url to scrape
            headers= {'User-Agent': 'Mozilla/5.0'}     # header parameter of the browser
            response = requests.get(url,headers=headers) # response contains data from the requests
            soup = BeautifulSoup(response.text, features="lxml")  # copy text of response to Beautiful soup
            
            # Beautiful soup parses html data
            table = soup.find('table')  # Find the table
            header = []                 # Init header list
            rows = []                   # Init rows
            # Iterate through all the table rows from HTML table
            # First row is the header
            for i, row in enumerate(table.find_all('tr')):
                if i == 0:
                    header = [el.text.strip() for el in row.find_all('th')]
                else:
                    rows.append([el.text.strip() for el in row.find_all('td')])
            
            # Copy the rows and header into the pandas dataframe
            tickers = pd.DataFrame(rows, columns=header)
            # Rename symbols with . to -
            tickers['Symbol'] = tickers['Symbol'].replace('BF.B', 'BF-B')
            tickers['Symbol'] = tickers['Symbol'].replace('BRK.B', 'BRK-B')

            # Save to csvfile                   
            TickersFile = f"data/tickers/symbols_{ndx}.csv"
            tickers.to_csv(TickersFile, index=False)           
            
            ticker_list = tickers['Symbol'].tolist()

        # Read 3 CSV files
        df1 = pd.read_csv(f"data/tickers/symbols_sp500.csv")
        df2 = pd.read_csv(f"data/tickers/symbols_nasdaq100.csv")
        df3 = pd.read_csv(f"data/tickers/symbols_dowjones.csv")   

        # Concatenate 'Symbol' columns from all dataframes
        combined_symbols = pd.concat([df1['Symbol'], df2['Symbol'], df3['Symbol']])

        # Remove duplicates
        unique_symbols = combined_symbols.drop_duplicates().reset_index(drop=True)
        unique_symbols.to_csv(f"data/tickers/symbols_all.csv")

        return unique_symbols
        

def slice_symbols(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Extract 'Symbol' column to a list
    symbols = df['Symbol'].tolist()
    
    # Slice the list into 101 rows each
    symb100 = [symbols[i:i+105] for i in range(0, len(symbols), 105)]
    
    return symb100


def download_and_process_symbols_data(symbols):
    # Download historical data for all symbols at once
    data = yf.download(symbols, start="2014-01-01", end="2024-12-31", group_by='ticker')
    
    # Iterate through each symbol to process and save its data
    for symbol in symbols:
        # Extract the data for the current symbol
        # Note: Need to handle cases where a single symbol is passed differently because yfinance structures the DataFrame differently for single vs multiple symbols.
        if len(symbols) > 1:
            symbol_data = data[symbol].drop(columns=['Adj Close'])
        else:
            symbol_data = data.drop(columns=['Adj Close'])
        
        # Round numerical values to two decimal places
        symbol_data = symbol_data.round(2)
        
        # Convert 'Volume' to millions and round to three decimal places
        symbol_data['Volume'] = (symbol_data['Volume'] / 1_000_000).round(3)
        
        # Save the processed data to a CSV file
        csv_filename = f"data/hist/{symbol}.csv"
        symbol_data.to_csv(csv_filename)
        print(f"All symbols:  {csv_filename}")

def download_summary_detail(symbols):
    data = Ticker(symbols)
    data_full = data.summary_detail

    print(data.summary_detail)   

    df = pd.DataFrame(data_full).T  # Transpose to get companies as rows
    print(df.tail())
    return df




def main():
    warnings.filterwarnings("ignore", category=FutureWarning)
    symbols = get_symbolss_tickers()
    print(symbols)
    csv_file_path = 'data/tickers/symbols_all.csv'
    symb100 = slice_symbols(csv_file_path)
    df0 = pd.DataFrame()   
    for s100 in symb100:
        symbols = s100  # This would print the first slice of 101 symbols
        download_and_process_symbols_data(symbols)
        #df1 = download_summary_detail(symbols)
        #df0 = pd.concat([df0,df1], ignore_index=True)
        print(df0.tail)
    #    

main()
