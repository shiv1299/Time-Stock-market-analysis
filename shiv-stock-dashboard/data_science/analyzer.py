"""
Stock analyzer - orchestrates all Data Science modules.
Django views call this; it remains independent of web framework.
"""
from typing import Optional, Dict, Any
import pandas as pd

from .data_fetcher import fetch_stock_data, get_company_info
from .trend_detection import detect_trend
from .price_prediction import predict_next_price
from .signal_generation import generate_signal


def analyze_stock(symbol: str) -> Optional[Dict[str, Any]]:
    """
    Run full analysis pipeline on a stock symbol.
    """

    # 🔹 Step 1 — Fetch historical data (Finnhub via data_fetcher)
    df = fetch_stock_data(symbol)

    if df is None or df.empty:
        print("Analyzer: No dataframe returned")
        return None

    # 🔹 Step 2 — Company info
    info = get_company_info(symbol)

    # fallback price
    if info['current_price'] is None and not df.empty:
        info['current_price'] = float(df['Close'].iloc[-1])

    prices = df['Close']

    # 🔹 Step 3 — Data science modules
    trend = detect_trend(prices)
    predicted_price, change_pct = predict_next_price(prices)
    signal = generate_signal(trend, change_pct)

    # 🔹 Step 4 — Chart data
    chart_df = df.tail(90)
    chart_data = [
        {
            'date': d.strftime('%Y-%m-%d'),
            'close': float(c),
        }
        for d, c in zip(chart_df.index, chart_df['Close'])
    ]

    # 🔹 Step 5 — Metrics
    if len(df) >= 2:
        day_change = (prices.iloc[-1] - prices.iloc[-2]) / prices.iloc[-2] * 100
    else:
        day_change = 0

    metrics = {
        'day_change_pct': round(day_change, 2),
        'volume': info.get('volume'),
        'previous_close': info.get('previous_close'),
    }

    # 🔹 Step 6 — Final response
    return {
        'symbol': symbol.upper(),
        'company_name': info['name'],
        'current_price': round(float(info['current_price'] or prices.iloc[-1]), 2),
        'metrics': metrics,
        'chart_data': chart_data,
        'trend': trend,
        'predicted_price': round(predicted_price, 2),
        'predicted_change_pct': round(change_pct, 2),
        'signal': signal,
    }