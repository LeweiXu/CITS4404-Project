import numpy as np
from utils.data_loader import read_csv
from optimisers.CCS import cyclic_coordinate_search
from bots.example_bot import simple_bot
from config import TRAINING_DATASET_PATH

data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2020-12-31")
params = cyclic_coordinate_search(simple_bot, data)
print(params)
