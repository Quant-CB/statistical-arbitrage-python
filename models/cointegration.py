import numpy as np
import pandas as pd
import yfinance as yf 
import statsmodels.api as sm

# Data Loader
def get_market_data(ticker1, ticker2, start_date="2024-01-01", end_date="2026-01-01"):
    # Download data and extract 'Close' prices directly
    df = yf.download([ticker1, ticker2], start=start_date, end=end_date, auto_adjust=True)
    
    # Handle different pandas / yfinance multi-index structures safely
    if 'Close' in df.columns:
        prices = df['Close']
    else:
        prices = df.xs('Close', level=1, axis=1)
        
    prices = prices.dropna()
    return prices


# Analyze OLS regression to find the hedge ratio (beta) and compute the rolling Z-Score
def analyze_pair(prices, stock_y, stock_x):
    y = prices[stock_y]
    x = prices[stock_x]

    X_model = sm.add_constant(x)
    ols = sm.OLS(y, X_model).fit()
    beta = ols.params.iloc[1]

    spread = y - (beta * x)

    window = 60
    mean = spread.rolling(window=window).mean()
    std = spread.rolling(window=window).std()
    z_score = (spread - mean) / std
    
    # Drop initial NaNs from rolling window
    z_score = z_score.dropna()

    # Return order matches the main assignment: beta first, then z_score
    return beta, z_score

if __name__ == "__main__":
    ticker_y = "AAPL"
    ticker_x = "MSFT"

    print(f"Downloading market data for {ticker_y} and {ticker_x}...")
    prices_df = get_market_data(ticker_y, ticker_x)

    beta, z_scores = analyze_pair(prices_df, ticker_y, ticker_x)
    
    print("\n-----------------------------------------")
    print("     Cointegration Analysis Results        ")
    print("-----------------------------------------")
    print(f"Hedge Ratio (Beta OLS): {beta:.4f}")
    print("\nLast 10 Z-Score values:")
    print(z_scores.tail(10))
