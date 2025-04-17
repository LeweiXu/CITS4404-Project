import numpy as np
from utils.data_loader import read_csv
from utils.trader import simulate_trades
from filters.wma import wma, sma_filter

class example_bot:
    """
    Example trading bot that uses a simple moving average crossover strategy.
    """
    def __init__(self, data, p1, p2):
        self.data = data
        self.p1 = p1
        self.p2 = p2

    def generate_signals(self):
        prices = self.data['close'].values

        # Calling wma() will automatically pad the prices
        sma_low = wma(prices, self.p1, sma_filter(self.p1))
        sma_high = wma(prices, self.p2, sma_filter(self.p2))

        # Generate buy (1) or sell (-1) signals based on SMA crossover
        signal = np.where(sma_low > sma_high, 1, 0)
        signals = np.diff(signal, prepend=0)
        return signals
    
    def bounds(self):
        """
        Returns the bounds for the parameters of the bot.
        """
        return {
            "p1": (1, 100),
            "p2": (1, 100)
        }

bot_instance = example_bot(
    data=read_csv("data/2020_hourly.csv"),
    p1=0,
    p2=0
)

def example_optimizer(bot):
    # optimiser p1 and p2