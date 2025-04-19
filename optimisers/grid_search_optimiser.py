import itertools
import numpy as np

def grid_search_optimiser(bot, training_data):
    """
    Optimizes the hyperparameters of a bot instance using a naive grid search approach.

    Parameters:
        bot (bot): An instance of the bot class.
        training_data (pd.DataFrame): The dataset containing price data.

    Returns:
        list: The best hyperparameters found during optimization.
    """
    param_ranges = []
    for bound in bot.bounds:
        if isinstance(bound, tuple):  # Continuous parameter
            # Discretize the range into 100 evenly spaced values
            param_ranges.append(np.linspace(bound[0], bound[1], 100))
        elif isinstance(bound, list):  # Discrete parameter
            param_ranges.append(bound)

    # Create a grid of all possible combinations
    all_combinations = list(itertools.product(*param_ranges))
    best_fitness = float('-inf')
    best_hyperparams = None

    # Test each combination of hyperparameters
    for hyperparams in all_combinations:
        bot.hyperparams = list(hyperparams)
        fitness = bot.fitness(training_data) 

        if fitness > best_fitness:
            best_fitness = fitness
            best_hyperparams = list(hyperparams)

    bot.hyperparams = best_hyperparams
    return best_hyperparams