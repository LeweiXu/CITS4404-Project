import numpy as np
from filters.wma import wma
from bots.bot_base import bot

class custom_wma_bot(bot):
    def __init__(self):
        self.hyperparams = []
        # Hyperparameters can either be discrete (define as list) or continuous (define as tuple)
        self.length = 50
        self.bounds = [(0,1) for j in range(0,2*self.length)] #[i/resolution for i in range(0, resolution+1)]

    def generate_signals(self, data):
        prices = data['close'].values

        wma_low = wma(prices, self.length, self.hyperparams[:self.length])
        wma_high = wma(prices, self.length, self.hyperparams[self.length:])

        # Generate buy (1) or sell (-1) signals based on WMA crossover
        signal = np.where(wma_low > wma_high, 1, 0)
        signals = np.diff(signal, prepend=0)
        return signals
    


