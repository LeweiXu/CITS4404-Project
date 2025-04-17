import numpy as np
from utils.data_loader import read_csv
from utils.trader import simulate_trades
from filters.wma import wma, sma_filter

# Each trading bot should have 2 functions: the optimization function and the generate_signals function
# Do whatever you want in the optimisation function
# The generate_signals function should return a numpy array of 1s (buy), -1s (sell) and 0s (hold) of the same length as the input data

def example_optimizer():
    """
    Optimises the hyperparameters p1 and p2 for the trading strategy.

    Returns:
        tuple: The optimal values for p1 and p2.
    """
    data = read_csv("data/BTC-Daily-2014-2019.csv", start_date="2015-01-01", end_date="2025-12-31") # Choose your training dataset
    p1, p2 = 10, 40
    best_cash = -np.inf
    best_p1, best_p2 = p1, p2

    for i in range(20):
        p1 += 1
        p2 += 1

        signals = generate_signals(data, "daily", p1, p2)
        final_cash = simulate_trades(data['close'].values, signals)

        if final_cash > best_cash:
            best_cash = final_cash
            best_p1, best_p2 = p1, p2

    return best_p1, best_p2

# This function must be able to take a dataframe of any length and return a signals of the same length
def generate_signals(data, granularity, p1=None, p2=None):
    """
    Generates trading signals based on the given hyperparameters.

    Parameters:
        data (pd.DataFrame): The dataset containing price data.
        p1 (float, optional): The window size for the short-term moving average.
        p2 (float, optional): The window size for the long-term moving average.

    Returns:
        np.ndarray: An array of trading signals.
    """
    # Basically, if this function is called without any parameters, it will run the optimisation algorithm to get them
    if p1 is None or p2 is None:
        p1, p2 = example_optimizer()

    prices = data['close'].values

    # Calling wma() will automatically pad the prices
    sma_low = wma(prices, p1, sma_filter(p1))
    sma_high = wma(prices, p2, sma_filter(p2))

    # Generate buy (1) or sell (-1) signals based on SMA crossover
    signal = np.where(sma_low > sma_high, 1, 0)
    signals = np.diff(signal, prepend=0)

    return signals