"""
Data fetcher module - fetches stock data from Alpha Vantage.
Kept separate from Django for pure Data Science logic.
"""
from typing import Optional
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("STOCK_API_KEY")


def fetch_stock_data(symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
    """
    Fetch historical stock data using Alpha Vantage daily adjusted endpoint.
    """
    try:
        # url = (
        #     "https://www.alphavantage.co/query"
        #     f"?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol.upper()}&outputsize=compact&apikey={api_key}"
        # )
        url = (
            "https://www.alphavantage.co/query"
            f"?function=GLOBAL_QUOTE&symbol={symbol.upper()}&apikey={api_key}"
        )
        response = requests.get(url)
        data = response.json()
        print("---------------------------")
        print("ALPHA DATA:", data)
        print("ALPHA DATA:", response)
        print("---------------------------")

        if "Time Series (Daily)" not in data:
            print("AlphaVantage error:", data)
            return None

        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")

        df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "6. volume": "Volume"
        }, inplace=True)

        df = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)

        if df.empty or len(df) < 5:
            return None

        return df

    except Exception as e:
        print("Fetch error:", e)
        return None


def get_company_info(symbol: str) -> dict:
    """
    Get basic company info using Alpha Vantage quote endpoint.
    """
    result = {
        'name': symbol.upper(),
        'current_price': None,
        'previous_close': None,
        'volume': None,
        'market_cap': None,
    }

    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=GLOBAL_QUOTE&symbol={symbol.upper()}&apikey={api_key}"
        )

        response = requests.get(url)
        data = response.json()

        print(response,data)

        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]

            result['current_price'] = float(quote.get("05. price", 0))
            result['previous_close'] = float(quote.get("08. previous close", 0))
            result['volume'] = int(quote.get("06. volume", 0))

    except Exception as e:
        print("Info error:", e)

    return result