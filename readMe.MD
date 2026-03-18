# Trading Strategy Backtester

A Python tool that backtests the Golden Cross / Death Cross moving average strategy on any stock ticker, comparing strategy performance against a simple buy & hold approach and visualizing buy/sell signals on an interactive chart.

## Features
- Golden Cross / Death Cross signal detection (50-day vs 200-day MA crossover)
- Buy & Hold vs Strategy profit comparison
- Win rate calculation across all trades
- Sharpe Ratio evaluation
- Interactive buy/sell signal chart
- Multi-ticker support in a single session
- Invalid ticker detection

## Technologies Used
- Python
- yfinance API
- pandas
- plotly.graph_objects

## How to Use
1. Clone the repository
2. Install dependencies: `pip install yfinance`, `pip install pandas`, `pip install plotly`
3. Run `python backtester.py`
4. Enter one or more stock tickers when prompted (e.g. `AAPL`, `TSLA`)
5. Type `STOP` when finished entering tickers
6. View printed performance stats and interactive charts for each ticker