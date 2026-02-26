"""
Trend detection module - identifies uptrend/downtrend from price history.
Uses moving averages and slope analysis.
"""
import pandas as pd
from typing import Tuple


def detect_trend(prices: pd.Series, short_window: int = 5, long_window: int = 20) -> str:
    """
    Detect market trend using moving average crossover and recent slope.
    
    Args:
        prices: Series of closing prices
        short_window: Short-term moving average window
        long_window: Long-term moving average window
    
    Returns:
        'Uptrend' or 'Downtrend'
    """
    if prices is None or len(prices) < long_window:
        return "Neutral"
    
    df = pd.DataFrame({'close': prices})
    
    df['sma_short'] = df['close'].rolling(window=short_window, min_periods=1).mean()
    df['sma_long'] = df['close'].rolling(window=long_window, min_periods=1).mean()
    
    # Current position: short above long = uptrend
    recent = df.tail(5)
    short_above_long = (recent['sma_short'] > recent['sma_long']).sum()
    
    # Slope of recent prices (last 10)
    if len(prices) >= 10:
        recent_prices = prices.tail(10).values
        slope = (recent_prices[-1] - recent_prices[0]) / recent_prices[0] if recent_prices[0] != 0 else 0
    else:
        slope = 0
    
    if short_above_long >= 3 and slope > 0:
        return "Uptrend"
    elif short_above_long <= 2 and slope < 0:
        return "Downtrend"
    elif slope > 0.02:
        return "Uptrend"
    elif slope < -0.02:
        return "Downtrend"
    
    return "Neutral"
