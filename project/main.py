import time
from fetcher.nse_client import NSEClient
from fetcher.nse_scrapper import NSEScrapper
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
client = NSEClient()

def display_table(df):
    table = Table(title="📊 Live Market Data via Google Finance (yfinance)", box=box.SIMPLE_HEAD)
    table.add_column("Symbol", justify="left")
    table.add_column("Price", justify="right")
    table.add_column("Change", justify="right")
    table.add_column("% Change", justify="right")

    for _, row in df.iterrows():
        table.add_row(
            row["symbol"],
            f'₹ {row["price"]:.2f}',
            f'{row["change"]:+.2f}',
            f'{row["percent_change"]:+.2f}%'
        )

    console.clear()
    console.print(table)

def display_scrapper_data():
    scrapper = NSEScrapper(interval=2)  # Refresh every 2 seconds
    while True:
        try:
            df = scrapper.fetch_nse_data()
            if not df.empty:
                df_display = df[["symbol", "lastPrice", "change", "pChange", "dayHigh", "dayLow", "totalTradedVolume"]]
                df_display.columns = ["Symbol", "LTP", "Change", "% Change", "High", "Low", "Volume"]
                console.clear()
                console.print(df_display.to_string(index=False))  # Display data
                console.print("\n⏱️ Updated every 2 seconds. Press Ctrl+C to stop.")
            else:
                console.print("[red]No data available[/red]")
            time.sleep(2)  # Refresh interval
        except KeyboardInterrupt:
            console.print("\n[bold red]Stopped by user.[/bold red]")
            break

# if __name__ == "__main__":
#     try:
#         while True:
#             df = client.get_market_data()
#             if not df.empty:
#                 display_table(df)
#             else:
#                 console.print("[red]No data available[/red]")
#             time.sleep(2)  # Refresh interval
#     except KeyboardInterrupt:
#         console.print("\n[bold red]Stopped by user.[/bold red]")

if __name__ == "__main__":
    try:
        display_scrapper_data()
    except KeyboardInterrupt:
        console.print("\n[bold red]Stopped by user.[/bold red]")