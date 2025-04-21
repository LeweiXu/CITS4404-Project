from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
from bots.macd_bot import macd_bot
from optimisers.grid_search_optimiser import grid_search_optimiser

macd_instance = macd_bot()
data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-12-31")
macd_instance.hyperparams = [21, 20, 5]
print(macd_instance.generate_signals(data))