from .bot_base import bot as Bot      # adjust import if different
from filters.wma import sma_filter, wma  # the helper filters
from config import TRAINING_DATASET_PATH
from utils.data_loader import read_csv
from optimisers.grid_search_optimiser import grid_search_optimiser
import numpy as np

class VinayakGWOBot(Bot):
    # --- set bounds for the optimiser ---
    # we’ll optimise two ints: N_short, N_long (window lengths)

    def __init__(self):
        self.hyperparams = []
        self.bounds = [[i for i in range(3, 26)], [i for i in range(30, 121)]]

    # main logic: given df + current params, spit out signals
    def generate_signals(self, data):
        N_short, N_long = self.hyperparams[0], self.hyperparams[1]

        # Calculate short and long moving averages
        short_ma = wma(data["close"].values, N_short, sma_filter(N_short))
        long_ma = wma(data["close"].values, N_long, sma_filter(N_long))

        # Calculate the difference between short and long moving averages
        diff = short_ma - long_ma

        # Generate buy/sell signals based on crossovers
        sig = np.zeros_like(diff)
        sig[1:] = np.where(
            (diff[1:] > 0) & (diff[:-1] <= 0), 1,  # Buy signal
            np.where((diff[1:] < 0) & (diff[:-1] >= 0), -1, 0)  # Sell signal
        )
        return sig
    
vinayak_gwo_bot_instance = VinayakGWOBot()
data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2019-12-31")
grid_search_optimiser(vinayak_gwo_bot_instance, data)