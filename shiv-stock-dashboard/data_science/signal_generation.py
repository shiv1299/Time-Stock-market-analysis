"""
Signal generation module - produces Buy / Hold / Sell recommendations.
Combines trend, prediction, and momentum.
"""
from typing import Optional


def generate_signal(
    trend: str,
    predicted_change_pct: float,
    current_price: Optional[float] = None,
    predicted_price: Optional[float] = None
) -> str:
    """
    Generate trading signal based on trend and prediction.
    
    Args:
        trend: 'Uptrend', 'Downtrend', or 'Neutral'
        predicted_change_pct: Expected percentage change from prediction model
        current_price: Optional current price
        predicted_price: Optional predicted price
    
    Returns:
        'Buy', 'Hold', or 'Sell'
    """
    # Strong buy: uptrend + significant positive prediction
    if trend == "Uptrend" and predicted_change_pct > 2.0:
        return "Buy"
    
    # Buy: uptrend or moderate positive prediction
    if trend == "Uptrend" and predicted_change_pct > -1.0:
        return "Buy"
    
    if trend == "Neutral" and predicted_change_pct > 3.0:
        return "Buy"
    
    # Strong sell: downtrend + significant negative prediction
    if trend == "Downtrend" and predicted_change_pct < -2.0:
        return "Sell"
    
    # Sell: downtrend or moderate negative prediction
    if trend == "Downtrend" and predicted_change_pct < 1.0:
        return "Sell"
    
    if trend == "Neutral" and predicted_change_pct < -3.0:
        return "Sell"
    
    return "Hold"
