import alpaca_trade_api as tradepi
import numpy as np
import time


SEC_KEY = "" # Enter secret key here!
PUB_KEY = "" # Enter public key here!
BASE_URL = "https://paper-api.alpaca.markets" # Base url for paper trading!

# For real trading don't enter the base url!
api = tradepi.REST(key_id = PUB_KEY, secret_key = SEC_KEY, base_url = BASE_URL)

# Buy a stock
api.submit_order(
    
    symbol = "GOOG", # Replace with ticker of stock you want to buy e.g. GOOG,BTCUSD
    qty = 1, # Amount
    side = "buy",
    type = "market",
    time_in_force = "gtc" # gtc = Good till Cancelled
    
    )

# Sell a stock

api.submit_order(
    
    symbol = "GOOG", # Replace with ticker of stock you want to buy e.g. GOOG,BTCUSD
    qty = 1, # Amount
    side = "sell",
    type = "market",
    time_in_force = "gtc" # gtc = Good till Cancelled
    
    )


# Read market data

symb = "GOOG"
pos_held = False

while True:
    print("")
    print("Checking Market Price")
    
    
    market_data = api.getbarset(symb, "minute", limit = 5) # Get one bar object of past 5 minutes
    
    close_list = [] # This array will store all the closing prices of bar's time interval
    for bar in market_data[symb]:
        close_list.append(bar.c) # bar.c is the closing price of bar's time interval
    
    close_list = np.array(close_list, dtype = np.float64) #Convert to numpy array
    ma = np.mean(close_list) # ma = Market average
    
    last_price = close_list[4] # Most recent closing price
    
    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))
    
    
    # Trading Strategy

    if ma + 1.0 < last_price and not pos_held: # If ma is more than 10cents under price and 
                                               # haven't been bought
        
        print("Buy")
        
        api.submit_order(
            
            symbol = "GOOG", # Replace with ticker of stock you want to buy e.g. GOOG,BTCUSD
            qty = 1, # Amount
            side = "buy",
            type = "market",
            time_in_force = "gtc" # gtc = Good till Cancelled
            
        )
        pos_held = True
        
    elif ma - 1.0 > last_price and pos_held: # If ma is more than 10cents under price and 
                                               # haven't been bought
        
        print("Sell")
        
        api.submit_order(
            
            symbol = "GOOG", # Replace with ticker of stock you want to buy e.g. GOOG,BTCUSD
            qty = 1, # Amount
            side = "sell",
            type = "market",
            time_in_force = "gtc" # gtc = Good till Cancelled
            
        )
        pos_held = False

        time.sleep(60) # Wait one minute before retrieving more market data
    


    
    
    
    
    
    




