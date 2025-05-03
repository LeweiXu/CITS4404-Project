from config import TRAINING_DATASET_PATH
from optimisers.hook_jeeves import hook_jeeves
from utils.data_loader import read_csv
from bots.bot_base import bot
from bots.simple_bot import simple_bot

# Hyperparameters can either be discrete (define as list) or continuous (define as tuple)
# e.g. a discrete parameter can be [1, 2, 3, 4, 5] or a continuous parameter can be (1, 10)
simple_bot_instance = simple_bot()
training_data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-12-31")
print(hook_jeeves(simple_bot_instance, training_data))
