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
        self.hyperparams = []
        # Define bounds for each hyperparameter
        self.bounds = [
            list(range(5, 51)),            # N_short: 5–50
            list(range(10, 101)),          # N_med  : 10–100
            list(range(20, 201)),          # N_long : 20–200
            [i/1000 for i in range(0, 51)], # threshold: 0.000–0.050
            list(range(1, 21)),            # momentum_period: 1–20
            [i/1000 for i in range(0, 101)],# momentum_th: 0.000–0.100
            list(range(1, 11)),            # rebuy_delay: 1–10 bars
        ]

    def generate_signals(self, data):
        prices = data['close'].values
        # Unpack and cast hyperparameters
        Ns, Nm, Nl, thr, mom_p, mom_th, delay = self.hyperparams
        Ns, Nm, Nl = map(lambda x: int(round(x)), (Ns, Nm, Nl))
        thr, mom_th = float(thr), float(mom_th)
        mom_p, delay = map(lambda x: int(round(x)), (mom_p, delay))

        # Ensure window ordering Ns < Nm < Nl
        if not (Ns < Nm < Nl):
            Nm = max(Ns + 1, min(Nm, Nl - 1))

        # Compute SMAs via convolution
        sma_short = wma(prices, Ns, sma_filter(Ns))
        sma_med   = wma(prices, Nm, sma_filter(Nm))
        sma_long  = wma(prices, Nl, sma_filter(Nl))

        signals = np.zeros(len(prices), dtype=int)
        last_buy = -np.inf

        for i in range(1, len(prices)):
            # Skip until indicators are valid
            if i < max(Nl, mom_p):
                continue

            # Compute relative differences between SMAs
            rel_sm = (sma_short[i] - sma_med[i]) / sma_med[i]
            rel_ml = (sma_med[i]   - sma_long[i]) / sma_long[i]

            # Compute momentum
            momentum = (prices[i] - prices[i - mom_p]) / prices[i - mom_p]

            # Buy condition: triple crossover + positive momentum + rebuy delay
            can_buy = (i - last_buy) >= delay
            if rel_sm > thr and rel_ml > thr and momentum > mom_th and can_buy:
                signals[i] = 1
                last_buy = i

            # Sell condition: reverse crossover + negative momentum
            elif rel_sm < -thr and rel_ml < -thr and momentum < -mom_th:
                signals[i] = -1

        return signals

gwo_bot_instance = gwo_bot()
training_data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2019-12-31")
best_value = gwo_optimiser(gwo_bot_instance, training_data,
                           num_wolves=30,   # pack size
                           max_iter=100)    # iterations
print("Best fitness:", best_value)
print("Best hyperparameters:", gwo_bot_instance.hyperparams)