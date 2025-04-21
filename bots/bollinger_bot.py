import numpy as np
import pandas as pd
from bots.bot_base import bot
from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
from optimisers.grid_search_optimiser import grid_search_optimiser


class bollinger_bot(bot):
    """
    Bollinger Band Bounce Strategy:
    - Hyperparameters:
      - N (window size in days): [10, 11, ..., 50]
      - K10 (bandwidth multiplier ×10): [15, 16, ..., 30], actual K = K10 / 10.0
    - Buy (+1) when the closing price falls below the lower band;
      Sell (-1) when it breaks above the upper band;
      Hold (0) otherwise.
    """

    def __init__(self):
        self.hyperparams = []
        # Use inclusive ranges
        self.bounds = [
            list(range(10, 51)),  # N: 10–50
            list(range(15, 31)),  # K10: 15–30 => K=1.5–3.0
        ]

    def generate_signals(self, data):
        # Ensure hyperparams are ints when needed
        N_raw, K10_raw = self.hyperparams
        N = int(round(N_raw))
        K10 = int(round(K10_raw))
        # Clip to valid bounds in case rounding moves out of range
        N = max(min(N, max(self.bounds[0])), min(self.bounds[0]))
        K10 = max(min(K10, max(self.bounds[1])), min(self.bounds[1]))

        prices = data["close"].values
        K = K10 / 10.0

        # Compute rolling statistics
        series = pd.Series(prices)
        rolling_mean = series.rolling(window=N, min_periods=1).mean().values
        rolling_std = series.rolling(window=N, min_periods=1).std(ddof=0).values

        upper = rolling_mean + K * rolling_std
        lower = rolling_mean - K * rolling_std

        # Raw signals: price < lower -> 1, price > upper -> -1, else 0
        raw = np.where(prices < lower, 1, np.where(prices > upper, -1, 0))

        # Convert to trading signals: signal changes
        signals = np.diff(raw, prepend=0)
        return signals


# ----------------------------------------
# Example usage: use grid search to optimize hyperparameters
bollinger_bot_instance = bollinger_bot()
training_data = read_csv(
    TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-12-31"
)
grid_search_optimiser(bollinger_bot_instance, training_data)
