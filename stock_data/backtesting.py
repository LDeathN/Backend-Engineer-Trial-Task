import pandas as pd
import numpy as np
from financial_data.stock_data.models import StockData


def get_stock_data(symbol):
    """Fetch historical stock data from the database."""
    return StockData.objects.filter(symbol=symbol).order_by('date')


def convert_to_dataframe(stock_data):
    """Convert queryset to pandas DataFrame."""
    data = pd.DataFrame(list(stock_data.values('date', 'close_price')))
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    return data


def calculate_moving_averages(data, short_window, long_window):
    """Calculate short and long moving averages."""
    data['short_mavg'] = data['close_price'].rolling(window=short_window, min_periods=1).mean()
    data['long_mavg'] = data['close_price'].rolling(window=long_window, min_periods=1).mean()
    return data


def generate_signals(data):
    """Generate buy/sell signals based on moving averages."""
    data['signal'] = 0
    data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1, 0)
    data['positions'] = data['signal'].diff()
    return data


def calculate_metrics(returns):
    """Calculate performance metrics."""
    total_return = (returns + 1).prod() - 1
    max_drawdown = (returns.cummax() - returns).max()
    num_trades = len(returns[returns != 0])
    return {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'num_trades': num_trades,
    }


def perform_backtesting(validated_data):
    """Perform backtesting using the validated input data."""
    initial_investment = validated_data['initial_investment']
    short_window = validated_data['short_window']
    long_window = validated_data['long_window']
    symbol = validated_data['symbol']

    # Fetch historical stock data
    stock_data = get_stock_data(symbol)
    if stock_data.exists():
        data = convert_to_dataframe(stock_data)
        data = calculate_moving_averages(data, short_window, long_window)
        data = generate_signals(data)

        # Simulate trading
        positions = initial_investment * data['signal']
        portfolio = positions * data['close_price']
        total_portfolio = portfolio.sum(axis=1)

        # Calculate returns
        returns = total_portfolio.pct_change()

        # Calculate metrics
        metrics = calculate_metrics(returns)
        return metrics
    else:
        return {"error": "No data available for the provided symbol."}

