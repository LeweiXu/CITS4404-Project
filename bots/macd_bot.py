import numpy as np
from bots.bot_base import bot
from filters.macd import macd
from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
from pantry.grid_search_optimiser import grid_search_optimiser
from utils.plots import plot_macd_with_signals

class macd_bot(bot):
    """
    MACD Strategy:
    - Hyperparameters:
      - fast_window: Fast EMA period
      - slow_window: Slow EMA period
      - signal_window: Signal line EMA period
    - Buy (+1) when the MACD line crosses above the Signal line;
      Sell (-1) when the MACD line crosses below the Signal line;
      Hold (0) otherwise.
    """

    def __init__(self):
        self.hyperparams = []
        self.bounds = [
            list(range(5, 31)),
            list(range(20, 61)), 
            list(range(5, 21)), 
        ]

    def generate_signals(self, data):
        fast_window, slow_window, signal_window = map(int, self.hyperparams)

        fast_window = max(min(fast_window, max(self.bounds[0])), min(self.bounds[0]))
        slow_window = max(min(slow_window, max(self.bounds[1])), min(self.bounds[1]))
        signal_window = max(min(signal_window, max(self.bounds[2])), min(self.bounds[2]))

        prices = data["close"].values

        macd_line, signal_line, _ = macd(prices, fast_window, slow_window, signal_window)

        signals = np.zeros_like(macd_line)

        buy_signals = (macd_line[1:] > signal_line[1:]) & (macd_line[:-1] <= signal_line[:-1])
        signals[1:][buy_signals] = 1

        sell_signals = (macd_line[1:] < signal_line[1:]) & (macd_line[:-1] >= signal_line[:-1])
        signals[1:][sell_signals] = -1

        # plot_macd_with_signals(data, macd_line, signal_line, signals, plot_name="macd_signals")
        return signals

macd_bot_instance = macd_bot()
training_data = read_csv(TRAINING_DATASET_PATH, start_date="2017-01-01", end_date="2018-12-31")
grid_search_optimiser(macd_bot_instance, training_data)