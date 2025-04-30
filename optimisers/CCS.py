def CCS(bot_instance, data, max_iterations=100, fit_history=False):
    """
    Optimizes the hyperparameters of a bot instance using Cyclic Coordinate Search.

    Parameters:
        bot_instance (bot): An instance of the bot class.
        data (pd.DataFrame): The dataset containing price data.
        max_iterations (int): The maximum number of iterations for optimization.

    Returns:
        list: The best hyperparameters found during optimization.
    """
    # Initialize hyperparameters at the midpoint of their bounds
    hyperparams = []
    for bound in bot_instance.bounds:
        if isinstance(bound, tuple):  # Continuous parameter
            hyperparams.append((bound[0] + bound[1]) / 2)
        elif isinstance(bound, list):  # Discrete parameter
            hyperparams.append(bound[len(bound) // 2])  # Midpoint of the list

    # Evaluate the initial fitness
    best_fitness = bot_instance.fitness(hyperparams, data)
    BestList = []
    for iteration in range(max_iterations):
        for i in range(len(bot_instance.bounds)):  # Cycle through each parameter
            # Try increasing the parameter
            new_hyperparams = hyperparams[:]
            if isinstance(bot_instance.bounds[i], tuple):  # Continuous parameter
                step_size = (bot_instance.bounds[i][1] - bot_instance.bounds[i][0]) * 0.1
                new_hyperparams[i] = min(new_hyperparams[i] + step_size, bot_instance.bounds[i][1])
            elif isinstance(bot_instance.bounds[i], list):  # Discrete parameter
                current_index = bot_instance.bounds[i].index(hyperparams[i])
                if current_index < len(bot_instance.bounds[i]) - 1:
                    new_hyperparams[i] = bot_instance.bounds[i][current_index + 1]

            # Evaluate the fitness of the new parameters
            new_fitness = bot_instance.fitness(new_hyperparams, data)
            if new_fitness > best_fitness:
                hyperparams = new_hyperparams
                best_fitness = new_fitness
                continue  # Skip decreasing if increasing improves the fitness

            # Try decreasing the parameter
            new_hyperparams = hyperparams[:]
            if isinstance(bot_instance.bounds[i], tuple):  # Continuous parameter
                step_size = (bot_instance.bounds[i][1] - bot_instance.bounds[i][0]) * 0.1
                new_hyperparams[i] = max(new_hyperparams[i] - step_size, bot_instance.bounds[i][0])
            elif isinstance(bot_instance.bounds[i], list):  # Discrete parameter
                current_index = bot_instance.bounds[i].index(hyperparams[i])
                if current_index > 0:
                    new_hyperparams[i] = bot_instance.bounds[i][current_index - 1]

            # Evaluate the fitness of the new parameters
            new_fitness = bot_instance.fitness(new_hyperparams, data)
            if new_fitness > best_fitness:
                hyperparams = new_hyperparams
                best_fitness = new_fitness
        BestList.append(best_fitness)
    
    if fit_history:
        return BestList
    else:
        return hyperparams