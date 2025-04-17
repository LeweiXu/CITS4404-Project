import numpy as np
from utils.trader import simulate_trades

def example_optimizer(bot, data, param_ranges, max_iterations=50):
    """
    Optimizes the parameters of a trading bot using a simple grid search.

    Parameters:
        bot (object): The trading bot object with a `generate_signals` method.
        data (pd.DataFrame): The dataset containing price data.
        param_ranges (dict): A dictionary where keys are parameter names and values are tuples of (min, max).
        max_iterations (int): The maximum number of iterations for optimization.

    Returns:
        dict: The best parameters for the bot.
    """
    # Initialize the best parameters and best fitness
    best_params = {param: None for param in param_ranges}
    best_fitness = -np.inf

    # Generate random candidate solutions
    for _ in range(max_iterations):
        # Randomly sample parameters within their ranges
        candidate_params = {param: np.random.uniform(*param_ranges[param]) for param in param_ranges}

        # Set the bot's parameters
        for param, value in candidate_params.items():
            setattr(bot, param, value)

        # Generate signals and evaluate the bot's performance
        signals = bot.generate_signals()
        fitness = simulate_trades(data['close'].values, signals)

        # Update the best parameters if the candidate is better
        if fitness > best_fitness:
            best_fitness = fitness
            best_params = candidate_params

    return best_params