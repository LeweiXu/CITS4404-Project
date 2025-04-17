import numpy as np
from utils.data_loader import read_csv
from utils.trader import simulate_trades
from filters.wma import wma, sma_filter


def abc_optimizer(num_bees=20, max_iterations=50):
    """
    Artificial Bee Colony (ABC) optimizer to find the best hyperparameters for the trading strategy.

    Parameters:
        data (pd.DataFrame): The dataset containing price data.
        num_bees (int): Number of bees in the colony.
        max_iterations (int): Maximum number of iterations.

    Returns:
        tuple: The optimal values for p1, p2, and threshold.
    """
    # Initialize the hyperparameter search space
    p1_range = (5, 50)  # Short-term moving average window size
    p2_range = (20, 100)  # Long-term moving average window size
    threshold_range = (0.01, 0.1)  # Threshold for generating signals

    data = read_csv("data/BTC-Daily-2014-2019.csv", start_date="2015-01-01", end_date="2025-12-31")  # Choose your training dataset

    # Initialize the bee population
    population = [
        {
            "p1": np.random.randint(*p1_range),
            "p2": np.random.randint(*p2_range),
            "threshold": np.random.uniform(*threshold_range),
            "fitness": -np.inf
        }
        for _ in range(num_bees)
    ]

    # Evaluate the initial population
    for bee in population:
        signals = generate_signals(data, "daily", bee["p1"], bee["p2"], bee["threshold"])
        bee["fitness"] = simulate_trades(data['close'].values, signals)

    # ABC optimization loop
    for iteration in range(max_iterations):
        for bee in population:
            # Generate a new candidate solution by modifying one parameter
            new_p1 = np.clip(bee["p1"] + np.random.randint(-5, 5), *p1_range)
            new_p2 = np.clip(bee["p2"] + np.random.randint(-5, 5), *p2_range)
            new_threshold = np.clip(bee["threshold"] + np.random.uniform(-0.01, 0.01), *threshold_range)

            # Evaluate the new solution
            signals = generate_signals(data, "daily", new_p1, new_p2, new_threshold)
            new_fitness = simulate_trades(data['close'].values, signals)

            # Replace the bee's solution if the new one is better
            if new_fitness > bee["fitness"]:
                bee["p1"] = new_p1
                bee["p2"] = new_p2
                bee["threshold"] = new_threshold
                bee["fitness"] = new_fitness

    # Return the best solution
    best_bee = max(population, key=lambda b: b["fitness"])
    return best_bee["p1"], best_bee["p2"], best_bee["threshold"]