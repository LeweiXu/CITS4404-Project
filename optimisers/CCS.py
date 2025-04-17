def cyclic_coordinate_search(bot_instance, data, max_iterations=100, step_size=0.1):
    """
    Optimizes the hyperparameters of a bot instance using Cyclic Coordinate Search.

    Parameters:
        bot_instance (bot): An instance of the bot class.
        data (pd.DataFrame): The dataset containing price data.
        max_iterations (int): The maximum number of iterations for optimization.
        step_size (float): The step size for adjusting each parameter.

    Returns:
        tuple: The best hyperparameters and the corresponding total return.
    """
    # Initialize hyperparameters at the midpoint of their bounds
    hyperparams = [(low + high) / 2 for low, high in bot_instance.bounds]
    best_return = bot_instance.total_return(hyperparams, data)

    for iteration in range(max_iterations):
        for i in range(bot_instance.n):  # Cycle through each parameter
            # Try increasing the parameter
            new_hyperparams = hyperparams[:]
            new_hyperparams[i] = min(new_hyperparams[i] + step_size, bot_instance.bounds[i][1])
            new_return = bot_instance.total_return(new_hyperparams, data)

            if new_return > best_return:
                hyperparams = new_hyperparams
                best_return = new_return
                continue  # Skip decreasing if increasing improves the return

            # Try decreasing the parameter
            new_hyperparams[i] = max(hyperparams[i] - step_size, bot_instance.bounds[i][0])
            new_return = bot_instance.total_return(new_hyperparams, data)

            if new_return > best_return:
                hyperparams = new_hyperparams
                best_return = new_return

    return hyperparams