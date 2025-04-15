import numpy as np

#Define filters here
def sma_filter(window):
    return np.ones(window) / window

def lma_filter(window):
    weights = np.arange(1, window + 1)
    return weights / weights.sum()

def ema_filter(window, alpha):
    weights = [(1 - alpha) ** k for k in range(window)]
    weights = np.array(weights)[::-1]
    return alpha * weights / sum(weights)

# Calculate the Weighted Moving Average (WMA)
def pad(prices,n):
    padding = -np.flip(prices[1:n])
    return np.append(padding, prices)

def wma(prices, n, kernel):
    """
    Calculate the Weighted Moving Average (WMA) of a given list of prices.
    The WMA is computed by convolving the input prices with a specified kernel
    after padding the prices to ensure the output has the same length as the input.
    Parameters:
        prices (list or numpy.ndarray): array of price values to calculate the WMA for.
        n (int): The window size for the WMA calculation.
        kernel (numpy.ndarray): the filter to use for the WMA calculation.
    Returns:
        numpy.ndarray: The Weighted Moving Average of the input prices.
    Note:
        - The `pad` function is assumed to handle the padding of the input prices.
    """

    padded = pad(prices, n)
    return np.convolve(padded, kernel, mode='valid')