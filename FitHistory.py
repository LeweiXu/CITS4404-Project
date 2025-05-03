import matplotlib.pyplot as plt
from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
#----------------Bots----------------
from bots.bollinger_bot import bollinger_bot


from bots.gwo_bot import gwo_bot
from bots.macd_bot import macd_bot
from bots.simple_bot import simple_bot
from bots.wma_rsi_bot import wma_rsi_bot
from bots.zero_cross_bot import zero_cross_bot
#----------------Optimisers----------------
from optimisers.gwo_optimiser import gwo_optimiser
from optimisers.pso_optimiser import pso_optimiser

data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-12-31")
bots = [bollinger_bot(), gwo_bot(), macd_bot(), simple_bot(), wma_rsi_bot(), zero_cross_bot()]

plt.figure(1)
for bot in bots:
    plt.plot(gwo_optimiser(bot, data, num_wolves=30, max_iter=100, fit_history = True))     #plots the fitness vs iteration using gwo



#plt.figure(2)
#for bot in bots:
#    plt.plot(pso_optimiser(bot, data, fit_history = True))     #plots the fitness vs iteration using pso

plt.show()