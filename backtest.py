import yfinance as yf
import pandas as pd
import plotly.express as px

def get_data(Token):
    data = yf.download(Token, period="10y")
    return data

df = get_data("AAPL")

df = df.reset_index()

df['MA_50'] = df['Close'].rolling(window=50).mean()
df['MA_200'] = df['Close'].rolling(window=200).mean()

in_trade = False
starting_price = 0
profit_tracker = []
totalNumTrades = 0

for i in range(len(df)):
    if in_trade == False and df['MA_50'].iloc[i-1] < df['MA_200'].iloc[i-1] and df['MA_200'].iloc[i] < df['MA_50'].iloc[i]:
        in_trade = True
        starting_price = df['Close'].iloc[i]
    elif in_trade == True and df['MA_50'].iloc[i-1] > df['MA_200'].iloc[i-1] and df['MA_200'].iloc[i] > df['MA_50'].iloc[i]:
        in_trade = False
        profit = df['Close'].iloc[i] - starting_price
        profit_tracker.append(profit.item())
        totalNumTrades += 1

hold_profit = (df['Close'].iloc[-1] - df['Close'].iloc[0]).item()

x = sum(profit_tracker)

print(f"Holding: {hold_profit}")
print(f"Trading: {x}")

if hold_profit > x:
    print("Hold the Stock")
elif x > hold_profit:
    print("Trade the Stock")
