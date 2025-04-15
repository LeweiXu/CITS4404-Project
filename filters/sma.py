import numpy as np

def sma_filter(window):
    return np.ones(window) / window
