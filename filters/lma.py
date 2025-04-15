import numpy as np

def lma_filter(window):
    weights = np.arange(1, window + 1)
    return weights / weights.sum()
