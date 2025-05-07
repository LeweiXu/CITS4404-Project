import numpy as np
from bots.bot_base import bot
from filters.wma import sma_filter, wma
from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
from optimisers.gwo_optimiser import gwo_optimiser

class gwo_bot(bot):
    """
    Triple SMA Crossover with Momentum Filter Strategy:
    -----------------------------------------------
    Hyperparameters:
      1. N_short        : Short SMA window (bars)
      2. N_med          : Medium SMA window
      3. N_long         : Long SMA window
      4. threshold      : Minimum relative SMA difference for crossover
      5. momentum_period: Lookback period for momentum calculation
      6. momentum_th    : Minimum relative momentum threshold
      7. rebuy_delay    : Minimum bars between successive buys
    """
    def __init__(self):
        super().__init__()
        # default hyperparameter values
        self.hyperparams = [10, 20, 50, 0.01, 14, 0.02, 5]
        # bounds for each hyperparameter (must match order in hyperparams)
        self.bounds = [
            list(range(5, 51)),            # N_short: 5–50
            list(range(10, 101)),          # N_med  : 10–100
            list(range(20, 201)),          # N_long : 20–200
            [i/100 for i in range(0, 51)], # threshold: 0.00–0.50
            list(range(1, 51)),            # momentum_period: 1–50
            [i/100 for i in range(0, 51)], # momentum_th: 0.00–0.50
            list(range(1, 51)),            # rebuy_delay: 1–50
        ]

    def generate_signals(self, data):
        prices = data['close'].values
        Ns, Nm, Nl, thr, mom_p, mom_th, delay = self.hyperparams
        Ns, Nm, Nl = map(int, (round(Ns), round(Nm), round(Nl)))
        mom_p, delay = map(int, (round(mom_p), round(delay)))
        thr, mom_th = float(thr), float(mom_th)

        # --- indicators ------------------------------------------------------
        sma_short = wma(prices, Ns, sma_filter(Ns))
        sma_med   = wma(prices, Nm, sma_filter(Nm))
        sma_long  = wma(prices, Nl, sma_filter(Nl))
        # ---------------------------------------------------------------------

        signals      = np.zeros(len(prices), dtype=int)
        last_trade   = -np.inf        # index of last BUY *or* SELL
        in_position  = False          # False = holding cash, True = holding asset

        for i in range(1, len(prices)):
            if i < max(Nl, mom_p):          # not enough history yet
                continue

            rel_sm = (sma_short[i]-sma_med[i])  / sma_med[i]
            rel_ml = (sma_med[i]  -sma_long[i]) / sma_long[i]
            momentum = (prices[i]-prices[i-mom_p]) / prices[i-mom_p]
            enough_time = (i - last_trade) >= delay

            # ------ BUY ------------------------------------------------------
            if (not in_position and enough_time and
                rel_sm > thr and rel_ml > thr and momentum > mom_th):
                signals[i] = 1
                in_position = True
                last_trade = i

            # ------ SELL -----------------------------------------------------
            elif (in_position and enough_time and
                  rel_sm < -thr and rel_ml < -thr and momentum < -mom_th):
                signals[i] = -1
                in_position = False
                last_trade = i

        return signals

# === Execution Block ===
gwo_bot_instance = gwo_bot()
training_data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2019-12-31")
best_value = gwo_optimiser(gwo_bot_instance, training_data,
                           num_wolves=30,   # pack size
                           max_iter=100)    # iterations

print("Best fitness:", best_value)
print("Best hyperparameters:", gwo_bot_instance.hyperparams)
