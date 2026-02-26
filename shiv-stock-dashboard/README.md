# Stock Market Analysis Dashboard

A minimal, Data Science-focused stock analysis web dashboard built with Django.

## Features

- **Landing page**: Dark theme, centered search for stock symbols
- **Company dashboard**: Company name, current price, basic metrics, price chart
- **Data Science outputs**: Trend (Uptrend/Downtrend), Price prediction, Signal (Buy/Hold/Sell)
- **No authentication**: Publicly accessible
- **Modular Data Science**: Trend detection, price prediction, signal generation kept separate from Django

## Setup

```bash
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Project Structure

```
├── data_science/          # Data Science modules (framework-agnostic)
│   ├── data_fetcher.py    # Fetches stock data via yfinance
│   ├── trend_detection.py # Moving average + slope analysis
│   ├── price_prediction.py# Linear extrapolation forecast
│   ├── signal_generation.py# Buy/Hold/Sell logic
│   └── analyzer.py       # Orchestrates all modules
├── dashboard/             # Django app (lightweight interface)
│   ├── views.py          # Thin layer calling data_science
│   └── templates/
├── stock_dashboard/       # Django project config
└── requirements.txt
```

## Routing

- Landing: `/`
- Company: `/company/<symbol>/`

## Data Source

Uses [yfinance](https://github.com/ranaroussi/yfinance) to fetch real stock data from Yahoo Finance (no API key required).
