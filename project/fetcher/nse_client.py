import yfinance as yf
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

class NSEClient:
    def __init__(self):
        self.symbols = {
            "RELIANCE": "RELIANCE.NS",
            "INFY": "INFY.NS",
            "TCS": "TCS.NS",
            "HDFCBANK": "HDFCBANK.NS",
            "SBIN": "SBIN.NS"
            # Add more as needed
        }

    def get_market_data(self):
        try:
            tickers = list(self.symbols.values())
            data = yf.download(tickers=tickers, period="1d", interval="10s", threads=True, progress=False)

            latest_data = data["Close"].iloc[-1]
            change_data = data["Close"].iloc[-1] - data["Open"].iloc[0]
            percent_change = (change_data / data["Open"].iloc[0]) * 100

            result = []
            for i, symbol in enumerate(tickers):
                stock = {
                    "symbol": list(self.symbols.keys())[i],
                    "price": latest_data[symbol],
                    "change": change_data[symbol],
                    "percent_change": percent_change[symbol]
                }
                result.append(stock)

            return pd.DataFrame(result)

        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return pd.DataFrame()