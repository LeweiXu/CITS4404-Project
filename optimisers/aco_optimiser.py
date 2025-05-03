import numpy as np


def aco_optimiser(bot_instance, data, ants=20, iterations=30, rho=0.1, fit_history=False):
    """
    Use Ant Colony Optimization (ACO) to optimize the hyperparameters of bot_instance.
    Parameters:
      - bot_instance: An instance of a strategy class that inherits from bot (must have bounds and fitness)
      - data: DataFrame used to evaluate fitness
      - ants: Number of ants per generation
      - iterations: Number of generations (iterations)
      - rho: Pheromone evaporation rate (0 < rho < 1)
    Returns:
      - best_params: List of best-found hyperparameters
    """
    # 1. Discretize the parameter space
    bounds = bot_instance.bounds  # [[v1_1,...],[v2_1,...]]
    num_params = len(bounds)
    grid = [list(b) for b in bounds]
    pheromones = [np.ones(len(vals)) for vals in grid]

    # 2. Iterative search
    best_params = None
    best_score = -np.inf

    bestList = []
    for _ in range(iterations):  # Removed trange -> regular range
        all_solutions = []
        all_scores = []
        for _ in range(ants):
            params = []
            for i, vals in enumerate(grid):
                tau = pheromones[i]
                probs = tau / tau.sum()
                idx = np.random.choice(len(vals), p=probs)
                params.append(vals[idx])
            bot_instance.hyperparams = params
            score = bot_instance.fitness(data)
            all_solutions.append(params)
            all_scores.append(score)
            if score > best_score:
                best_score = score
                best_params = params.copy()

        # Pheromone evaporation
        for i in range(num_params):
            pheromones[i] *= 1 - rho

        # Deposit pheromone
        idx_best = np.argmax(all_scores)
        for i, val in enumerate(all_solutions[idx_best]):
            j = grid[i].index(val)
            pheromones[i][j] += all_scores[idx_best] / best_score
        bestList.append(best_score)
    # 3. Assign best params
    bot_instance.hyperparams = best_params
    print(f"[ACO] Best params: {best_params}, best cash: {best_score:.2f}")
    if fit_history:
        return bestList
    else:
        return best_params
