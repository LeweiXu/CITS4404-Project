import numpy as np

def ema_filter(window, alpha):
    weights = [(1 - alpha) ** k for k in range(window)]
    weights = np.array(weights)[::-1]
    return alpha * weights / sum(weights)
