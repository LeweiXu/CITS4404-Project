import itertools, numpy as np
from utils.data_loader import read_csv
from bots.vinayak_gwo_bot import VinayakGWOBot

def optimise_daily_ma():
    bot  = VinayakGWOBot()
    data = read_csv("data/BTC-Daily-2014-2019.csv", granularity="daily")
    best_f, best_p = -np.inf, None
    for N_s, N_l in itertools.product(range(3,26), range(30,121)):
        if N_s >= N_l:      # skip invalid
            continue
        fitness = bot.evaluate(data, (N_s, N_l))   # uses built‑in simulate_trades
        if fitness > best_f:
            best_f, best_p = fitness, (N_s, N_l)
    print("Best params", best_p, "->", best_f)
    bot.best_params = best_p   # cache for leaderboard
    return bot

if __name__ == "__main__":
    optimise_daily_ma()
