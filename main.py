# Imports
import time
import polygon
import alpaca_trade_api as tradepi
import numpy as np

# API keys for accessing the Alpaca API
SEC_KEY = "Your Secret Key Here"
PUB_KEY = "Your Public Key Here"

# Base URL for the Alpaca API (paper trading)
BASE_URL = "https://paper-api.alpaca.markets" # Remove this url when trading with real money.

class App:
  
  def __init__(self):
        # Initialize the API client using the API keys and base URL
        self.api = tradepi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

        # Initialize a variable to track whether a position is held
        self.pos_held = False

  def buy(self, symbol, qty):
      # Submit a market order to buy the specified quantity of the given symbol
      self.api.submit_order(
          symbol=symbol,
          qty=qty,
          side="buy",
          type="market",
          time_in_force="gtc"
      )
      # Update the position held variable
      self.pos_held = True
    
  def sell(self, symbol, qty):
    # Submit a market order to sell the specified quantity of the given symbol
    self.api.submit_order(
        symbol=symbol,
        qty=qty,
        side="sell",
        type="market",
        time_in_force="gtc"
    )
    # Update the position held variable
    self.pos_held = False
    
  def check_price(self, symbol):
    # Create a Polygon client using the Alpaca API keys
    polygon_client = polygon.Client(api_key=PUB_KEY, secret_key=SEC_KEY)

    # Retrieve the bar data for the given symbol
    barset = polygon_client.barset(symbol, "minute", limit=5)
    bar_data = barset[symbol]

    # Extract the closing prices from the bar data
    close_list = [bar.c for bar in bar_data]

    # Convert the closing prices to a numpy array and compute the mean
    close_list = np.array(close_list, dtype=np.float64)
    ma = np.mean(close_list)

    # Get the last closing price
    last_price = close_list[4]

    # Print the moving average and last closing price
    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

def auto_trade(api, symbol, qty):
    # Get the current price of the stock
    price = api.get_last_trade(symbol).price

    # Set the target sell price to be 10% higher than the current price
    target_sell_price = price * 1.1

    # Set the stop loss price to be 10% lower than the current price
    stop_loss_price = price * 0.9

    # Submit a market order to buy the specified quantity of the given symbol
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="buy",
        type="market",
        time_in_force="gtc"
    )

    # Set a flag to track whether the stop loss has been triggered
    stop_loss_triggered = False

    # Run an infinite loop to check the price of the stock every 5 seconds
    while True:
        # Get the current price of the stock
        current_price = api.get_last_trade(symbol).price

        # Check if the stop loss has been triggered
        if current_price <= stop_loss_price:
            # Sell the stock if the stop loss has been triggered
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side="sell",
                type="market",
                time_in_force="gtc"
            )
            stop_loss_triggered = True
            break

        # Check if the target sell price has been reached
        if current_price >= target_sell_price:
            # Sell the stock if the target sell price has been reached
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side="sell",
                type="market",
                time_in_force="gtc"
            )
            break

        # Sleep for 5 seconds before checking the price again
        time.sleep(5)

    # Print a message indicating whether the stop loss was triggered
    if stop_loss_triggered:
        print("Stop loss triggered")
    else:
        print("Target sell price reached")

def main():
    # Create an instance of the App class
    app = App()

    # Run an infinite loop to accept user commands
    while True:
        print("Enter a command:")
        print("'buy' to buy a stock")
        print("'sell' to sell a stock")
        print("'check' to check the price of a stock")
        print("'auto' to automatically trade a stock")
        print("'exit' to exit the program")

        # Get the user's command
        command = input()

        # Process the command
        if command == "buy":
            print("Enter the ticker symbol of the stock you want to buy:")
            symbol = input()
            print("Enter the quantity of stock you want to buy:")
            qty = int(input())
            app.buy(symbol, qty)
        
        elif command == "sell":
            print("Enter the ticker symbol of the stock you want to sell:")
            symbol = input()
            print("Enter the quantity of stock you want to sell:")
            qty = int(input())
            app.sell(symbol, qty)
        
        elif command == "check":
            print("Enter the ticker symbol of the stock you want to check:")
            symbol = input()
            app.check_price(symbol)
        
        elif command == "auto":
            print("Enter the ticker symbol of the stock you want to trade:")
            symbol = input()
            print("Enter the quantity of stock you want to trade:")
            qty = int(input())
            auto_trade(app.api, symbol, qty)
        
        elif command == "exit":
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

