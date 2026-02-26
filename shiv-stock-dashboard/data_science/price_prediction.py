"""
Price prediction module - simple forecasting for next price movement.
Uses linear extrapolation and moving average momentum.
"""
import pandas as pd
import numpy as np
from typing import Tuple


def predict_next_price(prices: pd.Series, horizon: int = 5) -> Tuple[float, float]:
    """
    Predict next period price using linear trend and simple momentum.
    
    Args:
        prices: Series of closing prices
        horizon: Number of days ahead to predict (1 = next day)
    
    Returns:
        Tuple of (predicted_price, expected_change_percent)
    """
    if prices is None or len(prices) < 10:
        return 0.0, 0.0
    
    arr = prices.values
    current = arr[-1]
    
    # Linear regression on last 20 points
    n = min(20, len(arr))
    x = np.arange(n)
    y = arr[-n:]
    
    # Slope and intercept
    x_mean = x.mean()
    y_mean = y.mean()
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    
    if denominator != 0:
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        predicted = intercept + slope * (n - 1 + horizon)
    else:
        predicted = current
    
    # Blend with recent average to reduce noise
    recent_avg = arr[-5:].mean()
    predicted = 0.6 * predicted + 0.4 * recent_avg
    
    change_pct = ((predicted - current) / current * 100) if current != 0 else 0
    
    return float(predicted), float(change_pct)
