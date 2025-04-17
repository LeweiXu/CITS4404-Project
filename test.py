import numpy as np
from utils.data_loader import read_csv
from utils.trader import simulate_trades
from filters.wma import wma, sma_filter
from optimisers.CCS import cyclic_coordinate_search
from bots.Gerardbot import bot, filter
from config import TRAINING_DATASET_PATH

bot_instance = bot(
    function = filter,
    bounds = [(1, 100), (1, 100), (0.01, 0.1)]
)

data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2020-12-31")
params = cyclic_coordinate_search(bot_instance, data)
print(params)
