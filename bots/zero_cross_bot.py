import numpy as np
from filters.wma import wma, sma_filter
from bots.bot_base import bot
from config import TRAINING_DATASET_PATH
from utils.data_loader import read_csv
from optimisers.bf_optimiser import bf_optimiser
from utils.plots import plot

class zero_cross_bot(bot):
    def __init__(self, data):
        self.hyperparams = []
        upper_bound = 365
        self.bounds = [[i for i in range(1, upper_bound)], [i for i in range(1, upper_bound)]]

    def generate_signals(self, data):
        prices = data['close'].values
        p1, p2 = self.hyperparams[0], self.hyperparams[1]

        sma_short = wma(prices, p1, sma_filter(p1))
        sma_long = wma(prices, p2, sma_filter(p2))

        diff = sma_short - sma_long  # Difference between the two SMAs

        # Compute signal: 1 for cross above zero, -1 for cross below zero
        signal = np.sign(diff)
        signals = np.diff(signal, prepend=signal[0])  # Detect changes

        buy_signals = (signals > 0).astype(int)      # Crossed above zero, Buy
        sell_signals = (signals < 0).astype(int) * -1  # Crossed below zero, Sell

        final_signals = buy_signals + sell_signals  # Combine to get -1, 0, or 1
        return final_signals
    
training_data = read_csv(TRAINING_DATASET_PATH, start_date="2019-01-01", end_date="2019-12-31")
zero_cross_bot_instance = zero_cross_bot(training_data)
bf_optimiser(zero_cross_bot_instance, training_data)