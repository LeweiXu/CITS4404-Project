from utils.data_loader import read_csv
from bots.wma_rsi_bot import wma_rsi_bot
from optimisers.pso_optimiser import pso_optimiser

from config import TRAINING_DATASET_PATH, DATASET_2020_DAILY_PATH
from utils.plots import plot

# Hyperparameters can either be discrete (define as list) or continuous (define as tuple)
# e.g. a discrete parameter can be [1, 2, 3, 4, 5] or a continuous parameter can be (1, 10)
wma_rsi_bot_instance = wma_rsi_bot()

training_data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-12-31")
pso_optimiser(wma_rsi_bot_instance, training_data)
plot(training_data, wma_rsi_bot_instance.generate_signals(training_data),"pso_test")
print(wma_rsi_bot_instance.hyperparams)
print(wma_rsi_bot_instance.fitness(training_data))

test_data = read_csv(DATASET_2020_DAILY_PATH, start_date="2020-01-01", end_date="2020-12-31")
print(wma_rsi_bot_instance.fitness(test_data))