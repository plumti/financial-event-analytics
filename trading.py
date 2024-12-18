import os
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

# Load environment variables from .env file
load_dotenv()

ALPACA_CONFIG = {
    "API_KEY": "key",
    "API_SECRET": "secret",
    "PAPER": True
}

class StockMonitor(Strategy):
    def initialize(self):
        self.symbols = self.read_symbols_from_csv("data/symbols.csv")
        self.csv_filename = "/teamspace/studios/this_studio/crewai-groq-reddit/data/stock_holdings_status.csv"

        # Ensure the file exists, and if not, create it with headers
        if not os.path.exists(self.csv_filename):
            with open(self.csv_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Symbol", "Status", "Quantity"])
                
    def read_symbols_from_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        return df['company_name'].tolist()
    def on_trading_iteration(self):
        try:
            current_holdings = self.get_current_holdings()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.report_status(timestamp, current_holdings)
            self.output_results(timestamp, current_holdings)
        except Exception as e:
            self.log_message(f"Error occurred during trading iteration: {e}")

    def get_current_holdings(self):
        holdings = {}
        for symbol in self.symbols:
            position = self.get_position(symbol)
            if position:
                holdings[symbol] = position.quantity
            else:
                holdings[symbol] = 0
        return holdings

    def report_status(self, timestamp, holdings):
        try:
            with open(self.csv_filename, 'a', newline='') as file:
                writer = csv.writer(file)
                for symbol, quantity in holdings.items():
                    status = "held" if quantity > 0 else "not held"
                    writer.writerow([timestamp, symbol, status, quantity])
            self.log_message(f"Status reported at {timestamp}: {holdings}")
        except Exception as e:
            self.log_message(f"Error occurred while writing to CSV: {e}")

    def output_results(self, timestamp, holdings):
        print(f"Status reported at {timestamp}:")
        for symbol, quantity in holdings.items():
            status = "held" if quantity > 0 else "not held"
            print(f"{symbol}: {status}, Quantity: {quantity}")

if __name__ == "__main__":
    broker = Alpaca(ALPACA_CONFIG)
    trader = Trader()
    strategy = StockMonitor(broker=broker)
    trader.add_strategy(strategy)

    end_date = datetime.now() + timedelta(days=7)

    while datetime.now() < end_date:
        trader.run_all()
        trader.sleep(60)
