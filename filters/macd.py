import numpy as np
from filters.wma import ema_filter, wma, pad

def macd(prices, fast_window, slow_window, signal_window):
    """
    Calculate the MACD (Moving Average Convergence Divergence) and Signal Line.

    Parameters:
        prices (numpy.ndarray): Array of price values.
        fast_window (int): The window size for the fast EMA.
        slow_window (int): The window size for the slow EMA.
        signal_window (int): The window size for the signal line EMA.

    Returns:
        tuple: A tuple containing:
            - macd_line (numpy.ndarray): The MACD line (difference between fast and slow EMA).
            - signal_line (numpy.ndarray): The Signal Line (EMA of the MACD line).
            - macd_histogram (numpy.ndarray): The MACD Histogram (MACD line - Signal line).
    """
    fast_filter = ema_filter(fast_window, alpha=2 / (fast_window + 1))
    slow_filter = ema_filter(slow_window, alpha=2 / (slow_window + 1))

    fast_ema = wma(prices, fast_window, fast_filter)
    slow_ema = wma(prices, slow_window, slow_filter)

    macd_line = fast_ema - slow_ema 

    signal_filter = ema_filter(signal_window, alpha=2 / (signal_window + 1))
    signal_line = wma(macd_line, signal_window, signal_filter)

    macd_histogram = macd_line - signal_line 
    return macd_line, signal_line, macd_histogram