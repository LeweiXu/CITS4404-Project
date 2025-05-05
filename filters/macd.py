import numpy as np

def macd(prices, fast_window, slow_window, signal_window):
    """
    Calculate the MACD and Signal Line.

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
    def ema(prices, window):
        ema = np.zeros_like(prices)
        multiplier = 2 / (window + 1)
        ema[0] = prices[0]
        for i in range(1, len(prices)):
            ema[i] = (prices[i] - ema[i - 1]) * multiplier + ema[i - 1]
        return ema

    fast_ema = ema(prices, fast_window)
    slow_ema = ema(prices, slow_window)

    macd_line = fast_ema - slow_ema

    signal_line = ema(macd_line, signal_window)

    macd_histogram = macd_line - signal_line

    return macd_line, signal_line, macd_histogram