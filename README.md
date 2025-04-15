# CITS4404-Project

## A Trading Bot Optimization Algorithm

Dataset: https://www.kaggle.com/datasets/prasoonkottarathil/btcinusd

Possible hyperparameters:

N_short,        # Short MA window
N_long,         # Long MA window
filter_type_short,  # e.g., 0 = SMA, 1 = EMA, 2 = LMA
filter_type_long,
alpha_short,    # EMA decay (if used)
alpha_long,     # EMA decay (if used)
threshold,      # Optional crossover margin
smooth_window,  # Optional signal smoothing
rebuy_delay,    # Delay between trades
hold_threshold  # Minimum price drop to trigger sell