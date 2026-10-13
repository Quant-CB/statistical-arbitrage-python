import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm, rankdata

# Data Loader
def get_market_data(ticker1, ticker2, start_date="2024-01-01", end_date="2026-01-01"):
    
    df = yf.download([ticker1, ticker2], start=start_date, end=end_date, auto_adjust=True)
    
    if 'Close' in df.columns:
        prices = df['Close']
    else:
        prices = df.xs('Close', level=1, axis=1)
        
    prices = prices.dropna()
    return prices

# Copula ECDF Function
def to_percentile(series):
    n = len(series)
    return rankdata(series) / (n + 1)

# Analyze Copula Pair Function
def analyze_copula_pair(prices_df, stock_y, stock_x, upper_bound=0.95, lower_bound=0.05):
    
    returns = prices_df.pct_change().dropna()
    
    u_y = to_percentile(returns[stock_y])
    u_x = to_percentile(returns[stock_x])
    
    z_y = norm.ppf(u_y)
    z_x = norm.ppf(u_x)

    # Calculate correlation coefficient (rho) in normal space
    rho = np.corrcoef(z_y, z_x)[0, 1]

    # Calculate conditional probability using the bivariate normal CDF
    cond_prob = norm.cdf((z_y - rho * z_x) / np.sqrt(1 - rho**2))
    cond_prob_series = pd.Series(cond_prob, index=returns.index)

    signals = pd.Series(0, index=returns.index)
    signals[cond_prob_series > upper_bound] = -1  # Short signal
    signals[cond_prob_series < lower_bound] = 1   # Long signal 

    return rho, cond_prob_series, signals

if __name__ == "__main__":
    ticker_y = "V"
    ticker_x = "MA"

    print(f"Downloading market data for {ticker_y} and {ticker_x}...")
    prices_df = get_market_data(ticker_y, ticker_x)

    # Eseguiamo il motore della Copula
    rho, cond_probs, signals = analyze_copula_pair(prices_df, ticker_y, ticker_x)
    
    print("\n-----------------------------------------")
    print("        GAUSSIAN COPULA RESULTS         ")
    print("-----------------------------------------")
    print(f"Copula Correlation (Rho): {rho:.4f}")
    print("\nLast 10 Conditional Probabilities:")
    print(cond_probs.tail(10))
    
    latest_signal = signals.iloc[-1]
    print(f"\nLatest Signal for {ticker_y} vs {ticker_x}: {latest_signal}")
    
    if latest_signal == 1:
        print(f"-> ACTION: Long {ticker_y} / Short {ticker_x} (Asset undervalued)")
    elif latest_signal == -1:
        print(f"-> ACTION: Short {ticker_y} / Long {ticker_x} (Asset overvalued)")
    else:
        print("-> ACTION: No signal (Market dependency is normal).\n")
