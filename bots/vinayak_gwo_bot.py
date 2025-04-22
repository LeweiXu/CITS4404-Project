from bot_base import Bot        # adjust import if different
from filters.wma import sma, ema, lma   # the helper filters
import numpy as np

class VinayakGWOBot(Bot):
    # --- set bounds for the optimiser ---
    # we’ll optimise two ints: N_short, N_long (window lengths)
    param_bounds = [(3, 25), (30, 120)]   # can tweak later

    def __init__(self):
        super().__init__("vinayak_gwo_bot")   # name shown in leaderboard

    # main logic: given df + current params, spit out signals
    def generate_signals(self, data, params=None):
        if params is None:
            # if leaderboard calls with no params, fall back to saved best
            params = self.best_params
        N_short, N_long = params
        short_ma = sma(data["close"].values, N_short)
        long_ma  = sma(data["close"].values, N_long)
        diff     = short_ma - long_ma
        # buy when diff crosses up, sell when crosses down
        sig = np.zeros_like(diff)
        sig[1:]  = np.where((diff[1:] > 0) & (diff[:-1] <= 0),  1,
                   np.where((diff[1:] < 0) & (diff[:-1] >= 0), -1, 0))
        return sig
