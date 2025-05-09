import numpy as np

# Hook Jeeves optimization method
def hook_jeeves(bot_instance, data, max_iterations=100, step_size=1, reduction_factor=0.5, fit_history=False):
    """
    Perform Hook Jeeves optimization to tune the hyperparameters of the bot.

    Parameters:
        bot_instance: The bot object whose hyperparameters are to be optimized.
        data: The dataset to evaluate fitness.
        max_iterations: Maximum number of iterations for the optimization.
        step_size: Initial step size for exploring the parameter space.
        reduction_factor: Factor by which the step size is reduced after each iteration.
    """
    # Initialize hyperparameters and fitness
    hyperparams = []
    for i in range(len(bot_instance.bounds)):
        if isinstance(bot_instance.bounds[i], list):
            hyperparams.append(int(np.random.choice(bot_instance.bounds[i])))
        elif isinstance(bot_instance.bounds[i], tuple):
            discretized_bounds = np.linspace(bot_instance.bounds[i][0], bot_instance.bounds[i][1], num=300)
            hyperparams.append(float(np.random.choice(discretized_bounds)))
    bot_instance.hyperparams = hyperparams
    best_fitness = bot_instance.fitness(data)
    bestList = []
    for iteration in range(max_iterations):
        improved = False

        # Explore step: Try modifying each hyperparameter
        for i in range(len(hyperparams)):
            for direction in [-1, 1]:
                new_hyperparams = hyperparams[:]

                # Handle discrete and continuous bounds
                if isinstance(bot_instance.bounds[i], list):
                    current_index = bot_instance.bounds[i].index(hyperparams[i])
                    new_index = current_index + direction
                    if 0 <= new_index < len(bot_instance.bounds[i]):
                        new_hyperparams[i] = bot_instance.bounds[i][new_index]
                elif isinstance(bot_instance.bounds[i], tuple):
                    new_hyperparams[i] += direction * step_size
                    new_hyperparams[i] = max(min(new_hyperparams[i], bot_instance.bounds[i][1]), bot_instance.bounds[i][0])

                # Ensure new hyperparameters are within bounds
                bot_instance.hyperparams = new_hyperparams
                fitness = bot_instance.fitness(data)

                if fitness > best_fitness:
                    best_fitness = fitness
                    hyperparams = new_hyperparams
                    improved = True

        # If no improvement, reduce step size
        if not improved:
            step_size *= reduction_factor
        
        bestList.append(best_fitness)
        # Terminate if step size is too small
        if step_size < 1e-6:
            break

    # Set the bot's hyperparameters to the best found
    bot_instance.hyperparams = hyperparams
    if fit_history:
        return bestList
    else:
        return (hyperparams, best_fitness)