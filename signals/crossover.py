import numpy as np

def generate_signals(short_ma, long_ma):
    signal = np.where(short_ma > long_ma, 1, 0)
    position = np.diff(signal, prepend=0)
    return position
