import numpy as np
from utils.data_loader import read_csv
from utils.trader import simulate_trades
from filters.wma import wma, sma_filter
from optimisers.CCS import cyclic_coordinate_search

def filter(hyperparams, data):                          # a function defined by each person for their bot, takes n hyper parameters and a data set, returns a list of buy signals
    p1, p2, threshold = hyperparams[0], hyperparams[1], hyperparams[2]
    prices = data['close'].values

    sma_low = wma(prices, p1, sma_filter(p1))
    sma_high = wma(prices, p2, sma_filter(p2))

    signal = np.where((sma_low - sma_high) > threshold, 1, 0)
    signal = np.where((sma_high - sma_low) > threshold, -1, signal)

    signals = np.diff(signal, prepend = 0)
    return signals

class bot:
    def __init__(self, function, bounds):
        self.function = function
        self.bounds = bounds
        self.n = len(bounds)

    def generate_signals(self, hyperparams, data):
        return self.function(hyperparams, data)

    def total_return(self, hyperparams, data):
        self.signals = self.generate_signals(hyperparams, data)
        return simulate_trades(data['close'].values, self.signals)
