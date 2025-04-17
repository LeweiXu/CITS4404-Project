import numpy as np
from filters.wma import wma, sma_filter
from bots.bot_base import bot
    
def simple_signal_generator(hyperparams, data):
    prices = data['close'].values
    p1, p2 = hyperparams[0], hyperparams[1]

    # Calling wma() will automatically pad the prices
    sma_low = wma(prices, p1, sma_filter(p1))
    sma_high = wma(prices, p2, sma_filter(p2))

    # Generate buy (1) or sell (-1) signals based on SMA crossover
    signal = np.where(sma_low > sma_high, 1, 0)
    signals = np.diff(signal, prepend=0)
    return signals

# Create a bot instance a filter (the function that generates the signals) and the bounds of the parameters
# Hyperparameters can either be discrete (define as list) or continuous (define as tuple)
# e.g. a discrete parameter can be [1, 2, 3, 4, 5] or a continuous parameter can be (1, 10)
simple_bot = bot(
    simple_signal_generator,
    [[i for i in range(5, 101)], [i for i in range(5, 101)]])