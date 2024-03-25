import pandas as pd
import yfinance as yf
import os
import pandas_ta as ta
from icecream import ic
from tqdm import tqdm
import warnings

class Tickers:
    def __init__(self, name):
        self.name = name
        self.tickers = self.read_csv()

    def read_csv(self):
        try:
            path = f'data/tickers/{self.name}.csv'
            ic(path)
            return pd.read_csv(path)['Symbol'].tolist()
        except FileNotFoundError:
            ic(f"No ticker file found at {path}.")
            return []

class History:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = self.fetch()

    def fetch(self):
        path = f'data/history/{self.symbol}.csv'
        if os.path.exists(path):
            return pd.read_csv(path, index_col='Date', parse_dates=True)
        else:
            return self.fetch_yfinance()

    def fetch_yfinance(self):
        end_date = pd.Timestamp.now()
        start_date = end_date - pd.DateOffset(years=20)
        data = yf.download(self.symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        return data

class TechnicalIndicators:
    def __init__(self, data):
        self.data = data

    def calculate_sma(self, periods):
        for period in periods:
            self.data[f'SMA_{period}'] = self.data.ta.sma(close='Close', length=period)
        return self.data

    def calculate_roc(self, periods):
        for period in periods:
            self.data[f'ROC_{period}'] = self.data.ta.roc(close='Close', length=period)
        return self.data

def make_dirs():
    os.makedirs('data/sma/', exist_ok=True)
    os.makedirs('data/roc/', exist_ok=True)

def main():
    warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance.utils")
    symbols_path = f'data/tickers/symbols.csv'
    symbols = pd.read_csv(symbols_path)['Symbol'].tolist()
    sma_periods = [5, 10, 20, 50, 100, 200]
    roc_periods = [5, 10, 20, 50, 100, 200]

    ic.disable()
    for ticker in tqdm(symbols):
        history = History(ticker)
        ti = TechnicalIndicators(history.data)
        
        # Calculate SMA and ROC using pandas_ta
        sma_data = ti.calculate_sma(sma_periods)
        roc_data = ti.calculate_roc(roc_periods)
        
        # Save the results
        sma_data.to_csv(f'data/sma/{ticker}.csv')
        roc_data.to_csv(f'data/roc/{ticker}.csv')
    ic.enable()
    
if __name__ == "__main__":
    main()
