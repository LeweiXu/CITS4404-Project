# bots/daily_ma_bot.py
import numpy as np
from bots.bot_base import bot       # adjust import if path differs
from filters.wma import sma_filter, wma  # simple‑moving‑average helper
from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
from optimisers.grid_search_optimiser import grid_search_optimiser

class DailyMABot(bot):
    # --- define parameter bounds for optimiser ------------
    #           (lower , upper , is_int?)
    param_bounds = {
        "N_short": ( 5,  30, True),   # short MA window in days
        "N_long" : (20, 120, True)    # long  MA window
    }

    # -------------------------------------------------------
    def __init__(self, **params):
        super().__init__(**params)

    # mandatory method -------------------------------------
    def generate_signals(self, data):
        close = data["Close"].values

        n_s, n_l = int(self.params["N_short"]), int(self.params["N_long"])
        ma_short = wma(close, n_s, sma_filter(n_s))
        ma_long  = wma(close, n_l, sma_filter(n_l))

        diff = ma_short - ma_long
        signals = np.sign(np.diff(np.concatenate([[0], diff])))
        # convert sign change (+1 buy, -1 sell, 0 hold)
        return signals.astype(int)

# ---------- convenience function for leaderboard ----------
def generate_signals(data, **hyper):
    bot = DailyMABot(**hyper)          # hyper = {} when leaderboard calls it
    return bot.generate_signals(data)

daily_ma_bot_instance = DailyMABot()
data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2019-12-31")
grid_search_optimiser(daily_ma_bot_instance, data)