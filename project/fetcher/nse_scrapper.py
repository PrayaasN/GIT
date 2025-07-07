import requests
import time
import os
import pandas as pd

class NSEScrapper:
    def __init__(self, interval=10):
        self.interval = interval
        self.base_url = "https://www.nseindia.com"
        self.api_url = f"{self.base_url}/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": self.base_url,
            "Accept": "application/json",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def fetch_nse_data(self):
        # Set cookies by visiting homepage
        self.session.get(self.base_url, timeout=5)

        response = self.session.get(self.api_url, timeout=10)
        data = response.json()

        return pd.DataFrame(data['data'])

    def display_live_data(self):
        try:
            while True:
                self.clear_terminal()
                df = self.fetch_nse_data()
                df_display = df[["symbol", "lastPrice", "change", "pChange", "dayHigh", "dayLow", "totalTradedVolume"]]
                df_display.columns = ["Symbol", "LTP", "Change", "% Change", "High", "Low", "Volume"]

                print(df_display.head(20).to_string(index=False))  # Display top 20 rows
                print("\n⏱️ Updated every", self.interval, "seconds. Press Ctrl+C to stop.")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n🛑 Live feed stopped by user.")

# Run the live terminal display
if __name__ == "__main__":
    scrapper = NSEScrapper(interval=10)  # Refresh every 10 seconds
    scrapper.display_live_data()