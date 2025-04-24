import numpy as np
from filters.wma import wma, sma_filter
from config import TRAINING_DATASET_PATH
from optimisers.grid_search_optimiser import grid_search_optimiser
from utils.data_loader import read_csv
from bots.bot_base import bot

class simple_bot(bot):
    def __init__(self):
        self.hyperparams = []
        self.bounds = [[i for i in range(5, 101)], [i for i in range(5, 101)]]

    def generate_signals(self, data):
        prices = data['close'].values
        p1, p2 = self.hyperparams[0], self.hyperparams[1]

        # Calling wma() will automatically pad the prices
        sma_low = wma(prices, p1, sma_filter(p1))
        sma_high = wma(prices, p2, sma_filter(p2))

        # Generate buy (1) or sell (-1) signals based on SMA crossover
        signal = np.where(sma_low > sma_high, 1, 0)
        signals = np.diff(signal, prepend=0)
        return signals
    
# Hyperparameters can either be discrete (define as list) or continuous (define as tuple)
# e.g. a discrete parameter can be [1, 2, 3, 4, 5] or a continuous parameter can be (1, 10)
simple_bot_instance = simple_bot()
training_data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-12-31")
grid_search_optimiser(simple_bot_instance, training_data)