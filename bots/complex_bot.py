import numpy as np
from filters.wma import wma, sma_filter
from config import TRAINING_DATASET_PATH
from optimisers.grid_search_optimiser import grid_search_optimiser
from utils.data_loader import read_csv
from bots.bot_base import bot

class complex_bot(bot):
    def __init__(self):
        self.hyperparams = []
        # Hyperparameters can either be discrete (define as list) or continuous (define as tuple)
        self.bounds = [[i for i in range(5, 101)], [i for i in range(5, 101)]]

    def generate_signals(self, data, customParams = False):
        if customParams == False:
            if self.hyperparams != []:
                params = self.hyperparams
            else:
                params = [1,1,1,1,1] # change to generate random numbers within bounds
        else:
            params = customParams

        prices = data['close'].values

        p1, p2 = params[0], params[1]

        # Calling wma() will automatically pad the prices
        sma_low = wma(prices, p1, sma_filter(p1))
        sma_high = wma(prices, p2, sma_filter(p2))

        # Generate buy (1) or sell (-1) signals based on SMA crossover
        signal = np.where(sma_low > sma_high, 1, 0)
        signals = np.diff(signal, prepend=0)
        return signals
    


