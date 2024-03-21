import pandas as pd
import yfinance as yf
import os
import talib
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

class SMA:
    def __init__(self, data, periods):
        self.data = data
        self.periods = periods

    def calculate(self):
        for period in self.periods:
            sma_column_name = f'SMA{period}'
            self.data[sma_column_name] = self.data['Close'].rolling(window=period).mean()
        self.data = self.data.round(2)     
        return self.data

class ROC:
    def __init__(self, data, periods):
        self.data = data
        self.periods = periods

    def calculate(self):
        for period in self.periods:
            roc_column_name = f'ROC{period}'
            self.data[roc_column_name] = self.data['Close'].diff(period) / self.data['Close'].shift(period) * 100
        self.data = self.data.round(2)    
        return self.data

class Oscillators:
    def __init__(self, data, ticker):
        self.data = data
        self.symbol = ticker

    def calculate_indicators(self):
        try:
            self.data['RSI'] = talib.RSI(self.data['Close'].values, timeperiod=14)
        except Exception as e:
            ic("An error occurred:", e, self.symbol)
            pass

        self.data['slowk'], self.data['slowd'] = talib.STOCH(self.data['High'].values, 
                                                              self.data['Low'].values, 
                                                              self.data['Close'].values,
                                                              fastk_period=14, 
                                                              slowk_period=3, 
                                                              slowk_matype=0, 
                                                              slowd_period=3, 
                                                              slowd_matype=0)
        self.data['slowk'], self.data['slowd']

        self.data['macd'], self.data['macdsignal'], self.data['macdhist'] = talib.MACD(self.data['Close'].values, 
                                                                                        fastperiod=12, 
                                                                                        slowperiod=26, 
                                                                                        signalperiod=9)
    
        self.data['CCI'] = talib.CCI(self.data['High'].values, 
                                     self.data['Low'].values, 
                                     self.data['Close'].values, 
                                     timeperiod=14)
    
        self.data['Williams %R'] = talib.WILLR(self.data['High'].values, 
                                               self.data['Low'].values, 
                                               self.data['Close'].values, 
                                               timeperiod=14)
    
        self.data['upperband'], self.data['middleband'], self.data['lowerband'] = talib.BBANDS(
            self.data['Close'].values,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0
        )
    
    def save_csv(self):
        self.calculate_indicators()
        filepath = f'datc/osci/{self.symbol}.csv'
        # List of columns you want to save
        columns_to_save = ['RSI','slowk','slowd','macd','macdsignal','macdhist','CCI','Williams %R','upperband','middleband','lowerband']    
        # Select only the columns you want to save
        selected_data = self.data[columns_to_save]
        selected_data = selected_data.round(2)
        selected_data.to_csv(filepath, index=True)
       
        #ic(f'Saved volume indicators to {filepath}')
       



class Volume:
    def __init__(self, data, symbol):
        self.data = data
        self.symbol = symbol

    def calculate_indicators(self):
        # Volume
        self.data['Volume_raw'] = self.data['Volume']

        # On-Balance Volume (OBV)
        self.data['OBV'] = talib.OBV(self.data['Close'], self.data['Volume'])

        # Volume Price Trend (VPT)
        self.data['VPT'] = (self.data['Volume'] * ((self.data['Close'] - self.data['Close'].shift(1)) / self.data['Close'].shift(1))).cumsum()

        # Accumulation/Distribution Line (A/D Line)
        clv = ((self.data['Close'] - self.data['Low']) - (self.data['High'] - self.data['Close'])) / (self.data['High'] - self.data['Low'])
        clv.fillna(0, inplace=True)  # replace NaN values with 0
        self.data['AD_Line'] = (clv * self.data['Volume']).cumsum()

        # Chaikin Money Flow (CMF)
        self.data['CMF'] = talib.ADOSC(self.data['High'], self.data['Low'], self.data['Close'], self.data['Volume'], fastperiod=3, slowperiod=10)

        # Money Flow Index (MFI)
        self.data['MFI'] = talib.MFI(self.data['High'], self.data['Low'], self.data['Close'], self.data['Volume'], timeperiod=14)

        # Volume Oscillator (VO)
        ma5 = talib.MA(self.data['Volume'], timeperiod=5, matype=0)
        ma10 = talib.MA(self.data['Volume'], timeperiod=10, matype=0)
        self.data['VO'] = ma5 - ma10

        # Klinger Oscillator (KO)
        self.data['DailyPriceChange'] = self.data['Close'] - self.data['Close'].shift(1)
        self.data['VolumeForce'] = self.data['DailyPriceChange'] * self.data['Volume']
        ema_short = self.data['VolumeForce'].ewm(span=34, adjust=False).mean()
        ema_long = self.data['VolumeForce'].ewm(span=55, adjust=False).mean()
        self.data['KO'] = ema_short - ema_long
        self.data.drop(['DailyPriceChange', 'VolumeForce'], axis=1, inplace=True)

    def save_csv(self):
        self.calculate_indicators()
        filepath = f'datc/volu/{self.symbol}.csv'
        # List of columns you want to save
        columns_to_save = ['Volume_raw', 'OBV', 'VPT', 'AD_Line', 'CMF', 'MFI', 'VO', 'KO']    
        # Select only the columns you want to save
        selected_data = self.data[columns_to_save]
        selected_data = selected_data.round(2)
       
       
        selected_data.to_csv(filepath, index=True)  
        ic(f'Volume indicators to {filepath}')



class Volatility:
    def __init__(self, data, symbol, datapath='datc/vola/'):
        self.data = data
        self.symbol = symbol
        self.datapath = datapath

    def calculate_indicators(self):
        # Average True Range (ATR)
        self.data['ATR'] = talib.ATR(self.data['High'], self.data['Low'], self.data['Close'], timeperiod=14)

        # Bollinger Bands
        upperband, middleband, lowerband = talib.BBANDS(self.data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        self.data['UpperBB'], self.data['MiddleBB'], self.data['LowerBB'] = upperband, middleband, lowerband

        # Standard Deviation of returns
        self.data['StdDev'] = self.data['Close'].pct_change().rolling(window=20).std()

    def save_csv(self):
        self.calculate_indicators()
        filepath = f'{self.datapath}{self.symbol}.csv'
        columns_to_save = ['ATR','UpperBB','MiddleBB','LowerBB','StdDev']
        selected_data = self.data[columns_to_save]
        selected_data = selected_data.round(2)
        selected_data.to_csv(filepath, index=True)
        ic(f'Volatility indicators to {filepath}')

class Candlestick:
    def __init__(self, data, ticker):
        self.data = data
        self.ticker = ticker

    def calculate_patterns(self):
        # Dictionary to hold our pattern functions
        pattern_functions = {
            'Hammer': talib.CDLHAMMER,
            'HamInv': talib.CDLINVERTEDHAMMER,
            'Doji': talib.CDLDOJI,
            'Engulfing': talib.CDLENGULFING,
            #'EngulfBul': talib.CDLBULLISHENGULFING,
            #'EngulfBer': talib.CDLBEARISHENGULFING,
            'StarMorn': talib.CDLMORNINGSTAR,
            'StarEvng': talib.CDLEVENINGSTAR,
            'StarShtg': talib.CDLSHOOTINGSTAR,
            'ThreeWS': talib.CDL3WHITESOLDIERS,
            'ThreeBC': talib.CDL3BLACKCROWS
        }

        # Initialize a DataFrame to hold all pattern indicators
        patterns_df = pd.DataFrame(index=self.data.index)

        # Calculate each pattern and add it to the DataFrame
        for name, func in pattern_functions.items():
            patterns_df[name] = func(self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'])

        # Merge pattern indicators back to the main data DataFrame
        self.data = pd.concat([self.data, patterns_df], axis=1)

    def save_csv(self):
        self.calculate_patterns()
        datapath = 'datc/candle/'
        filepath = f'{datapath}{self.ticker}.csv'
        columns_to_save = ['Hammer','Doji','Engulfing']
        selected_data =self.data[columns_to_save]
        selected_data.to_csv(filepath, index=True)
        ic(f'Candlestick patterns to {filepath}')

def make_dirs():
    os.makedirs('datc/sma/', exist_ok=True)    
    os.makedirs('datc/roc/', exist_ok=True)
    os.makedirs('datc/osci/', exist_ok=True)
    os.makedirs('datc/volu/', exist_ok=True)
    os.makedirs('datc/vola/', exist_ok=True)
    os.makedirs('datc/candle/', exist_ok=True)

def main():


    #tickers_name = "megacap"                
    #tickers_name = "slickchart_sp500"
    #tickers = Tickers('slickchart_sp500')        # 500+ stocks
    warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance.utils")
    proj_path = '/home/larry/atapps/aStockTrading'
    symbols_path = f'{proj_path}/data/tickers/symbo.csv'
    symbols = pd.read_csv(symbols_path)['Symbol'].tolist()
    sma_periods = [5, 10, 20, 50, 100, 200]
    roc_periods = [5, 10, 20, 50, 100, 200]

    ic.disable()
    for ticker in tqdm(symbols):
        history = History(ticker)
        
        sma = SMA(history.data, sma_periods)
        sma_data = sma.calculate()
        sma_data[[f'SMA{period}' for period in sma_periods]].to_csv(f'datc/sma/{ticker}.csv')
        
        roc = ROC(history.data, roc_periods)
        roc_data = roc.calculate()
        roc_data[[f'ROC{period}' for period in roc_periods]].to_csv(f'datc/roc/{ticker}.csv')

        oscillators = Oscillators(history.data, ticker)        
        oscillators.save_csv()

        volume = Volume(history.data, ticker)
        volume.save_csv()

        volatility = Volatility(history.data, ticker)
        volatility.save_csv()

        candlestick = Candlestick(history.data, ticker)
        candlestick.save_csv()
    ic.enable()

    
if __name__ == "__main__":
    main()
