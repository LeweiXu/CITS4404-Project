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
    padded = pad(prices, n)
    return np.convolve(padded, kernel, mode='valid')