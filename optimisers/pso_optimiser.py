import numpy as np


def enhanced_pso(fitness_func, lb, ub, swarmsize=30, maxiter=50,
                 initial_inertia=0.9, final_inertia=0.4,
                 cognitive=1.5, social=1.5, max_velocity_ratio=0.2,
                 early_stopping=None, verbose=True):
    """
    Enhanced PSO implementation with:
    - Dynamic inertia weight
    - Velocity clamping
    - Early stopping
    - Progress tracking
    """
    dim = len(lb)
    lb = np.array(lb)
    ub = np.array(ub)
    search_range = ub - lb

    # Initialize particles
    pos = np.random.uniform(lb, ub, (swarmsize, dim))
    vel = np.random.uniform(-search_range, search_range, (swarmsize, dim)) * 0.1

    # Velocity limits
    max_velocity = max_velocity_ratio * search_range
    min_velocity = -max_velocity

    # Initialize best positions and values
    pbest_pos = pos.copy()
    pbest_val = np.array([fitness_func(p) for p in pos])
    gbest_idx = np.argmin(pbest_val)
    gbest_pos = pbest_pos[gbest_idx].copy()
    gbest_val = pbest_val[gbest_idx]

    # Track convergence
    convergence_history = []
    no_improvement_count = 0

    # Iteration loop with progress bar
    #iter_range = tqdm(range(maxiter)) if verbose else range(maxiter)
    iter_range = range(maxiter)

    for iter in iter_range:
        # Linearly decreasing inertia
        inertia = initial_inertia - (initial_inertia - final_inertia) * (iter / maxiter)

        for i in range(swarmsize):
            # Update velocity with clamping
            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            vel[i] = (inertia * vel[i] +
                      cognitive * r1 * (pbest_pos[i] - pos[i]) +
                      social * r2 * (gbest_pos - pos[i]))

            # Apply velocity limits
            vel[i] = np.clip(vel[i], min_velocity, max_velocity)

            # Update position
            pos[i] += vel[i]

            # Boundary handling
            pos[i] = np.clip(pos[i], lb, ub)

            # Evaluate fitness
            fitness = fitness_func(pos[i])

            # Update personal best
            if fitness < pbest_val[i]:
                pbest_val[i] = fitness
                pbest_pos[i] = pos[i].copy()

                # Update global best
                if fitness < gbest_val:
                    gbest_val = fitness
                    gbest_pos = pos[i].copy()
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1

        convergence_history.append(gbest_val)

        # Early stopping check
        if early_stopping and no_improvement_count >= early_stopping:
            if verbose:
                print(f"Early stopping at iteration {iter}")
            break

    return {
        'best_position': gbest_pos,
        'best_fitness': gbest_val,
        'convergence_history': convergence_history,
        'n_iterations': iter + 1
    }


def pso_optimiser(bot_instance, data, swarmsize=30, maxiter=50, fit_history=False):
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

    # Use custom PSO implementation
    #best_params, best_fitness = enhanced_pso(pso_fitness, lb, ub, swarmsize=swarmsize, maxiter=maxiter)

    # 修改這行調用代碼
    result = enhanced_pso(pso_fitness, lb, ub, swarmsize=swarmsize, maxiter=maxiter)
    best_params = result['best_position']
    best_fitness = result['best_fitness']
    bestList = result['convergence_history']
    # Save the best parameters back to the bot instance
    bot_instance.hyperparams = best_params

    # Print the results
    print(f"[PSO] Best Params: {best_params}")
    print(f"[PSO] Final Cash: {-best_fitness:.2f}")  # Fitness is negated cash, so we convert back to positive

    if fit_history:
        return bestList
    else:
        return best_params

