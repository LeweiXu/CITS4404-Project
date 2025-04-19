from pyswarm import pso

def pso_optimiser(bot_instance, data, swarmsize=30, maxiter=50):
    """
    General PSO optimizer that supports any number of parameters.
    """

    # Define the fitness function (PSO minimizes by default, so we negate the fitness)
    def pso_fitness(params):
        bot_instance.hyperparams = params
        return -bot_instance.fitness(data)

    # Extract lower and upper bounds from the bot's parameter bounds
    lb = [b[0] if isinstance(b, tuple) else min(b) for b in bot_instance.bounds]
    ub = [b[1] if isinstance(b, tuple) else max(b) for b in bot_instance.bounds]

    # Run the PSO algorithm
    best_params, best_fitness = pso(pso_fitness, lb, ub, swarmsize=swarmsize, maxiter=maxiter)

    # Save the best parameters back to the bot instance
    bot_instance.hyperparams = best_params

    # Print the results
    print(f"[PSO] Best Params: {best_params}")
    print(f"[PSO] Final Cash: {-best_fitness:.2f}")  # Fitness is negated cash, so we convert back to positive

    return best_params
