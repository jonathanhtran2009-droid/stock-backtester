import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_data(Token):
    data = yf.download(Token, period="10y")
    return data

def when_buy_sell(df):
    in_trade = False
    starting_price = 0
    profit_tracker = []
    buyPoints = {}
    sellPoints = {}
    for i in range(len(df)):
        if in_trade == False and df['MA_50'].iloc[i-1] < df['MA_200'].iloc[i-1] and df['MA_200'].iloc[i] < df['MA_50'].iloc[i]:
            in_trade = True
            starting_price = df['Close'].iloc[i]
            buyPoints[df['Date'].iloc[i]] = df['Close'].iloc[i].item()
        elif in_trade == True and df['MA_50'].iloc[i-1] > df['MA_200'].iloc[i-1] and df['MA_200'].iloc[i] > df['MA_50'].iloc[i]:
            in_trade = False
            profit = df['Close'].iloc[i] - starting_price
            profit_tracker.append(profit.item())
            sellPoints[df['Date'].iloc[i]] = df['Close'].iloc[i].item()
    return profit_tracker, buyPoints, sellPoints

def sharpe(profit_tracker):
    return (pd.Series(profit_tracker).mean() - 0.04) / pd.Series(profit_tracker).std()

def hold_or_trade(df, profit_tracker, token):
    hold_profit = (df['Close'].iloc[-1] - df['Close'].iloc[0]).item()
    x = sum(profit_tracker)
    Winning_Trades = [t for t in profit_tracker if t > 0]
    Win_Rate = (len(Winning_Trades)/len(profit_tracker)) * 100

    print(f"=== {token} ===")
    print(f"Buy & Hold: {hold_profit}")
    print(f"Strategy: {x}")
    print(F"Win Rate: {Win_Rate}%")
    if hold_profit > x:
        print("Verdict: Hold the Stock")
    elif x > hold_profit:
        print("Verdict: Trade the Stock")

    print(f"Sharpe: {sharpe(profit_tracker):.2f}")

def show_graph(df, buyPoints, sellPoints, token):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'].squeeze(), y=df['Close'].squeeze(), mode='lines', name='Price'))
    fig.add_trace(go.Scatter(x=list(buyPoints.keys()), y=list(buyPoints.values()), mode='markers', name='Buy', marker=dict(size=10, color='green')))
    fig.add_trace(go.Scatter(x=list(sellPoints.keys()), y=list(sellPoints.values()), mode='markers', name='Sell', marker=dict(size=10, color='red')))

    fig.update_layout(
    xaxis_title="Date", 
    yaxis_title="Price",
    title=f"{token}, when to buy and sell"
    )
    fig.show()

Tokens = []

while True:
    Token = input("Input a ticker, STOP to stop: ").upper().strip()
    if Token == "STOP":
        break
    else:
        Tokens.append(Token)

for token in Tokens:
    df = get_data(token)

    if df.empty ==  True:
        continue
    else:
        df = df.reset_index()

        df['MA_50'] = df['Close'].rolling(window=50).mean()
        df['MA_200'] = df['Close'].rolling(window=200).mean()

        profit_tracker, buyPoints, sellPoints = when_buy_sell(df)
        hold_or_trade(df, profit_tracker, token)
        show_graph(df, buyPoints, sellPoints, token)