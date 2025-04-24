import numpy as np

def gwo_optimiser(bot, data, num_wolves=20, max_iter=50):
    """
    Grey Wolf Optimizer for bot hyperparameters.
    bot: an instance with .bounds (list of value-lists), .fitness(data), and .hyperparams
    data: the training data passed to bot.fitness
    num_wolves: pack size
    max_iter: number of iterations
    Returns the best fitness found.
    """

    dim = len(bot.bounds)
    # Initialize wolf positions randomly within bounds
    positions = np.zeros((num_wolves, dim))
    for d in range(dim):
        positions[:, d] = np.random.choice(bot.bounds[d], size=num_wolves)

    # Alpha, Beta, Delta trackers
    alpha_pos, alpha_score = None, -np.inf
    beta_pos,  beta_score  = None, -np.inf
    delta_pos, delta_score = None, -np.inf

    # Main loop
    for t in range(max_iter):
        a = 2 * (1 - t / (max_iter - 1))  # a decreases linearly from 2 to 0

        # 1) Evaluate fitness and update alpha/beta/delta
        for i in range(num_wolves):
            # Clip & cast into valid range before evaluation
            candidate = []
            for d in range(dim):
                col = bot.bounds[d]
                val = positions[i, d]
                # Ensure within [min,max]
                val = max(min(val, max(col)), min(col))
                # snap to nearest if discrete
                if all(isinstance(x, int) for x in col):
                    val = int(round(val))
                candidate.append(val)

            bot.hyperparams = candidate
            fit = bot.fitness(data)

            if fit > alpha_score:
                alpha_score, alpha_pos = fit, positions[i].copy()
            elif fit > beta_score:
                beta_score, beta_pos = fit, positions[i].copy()
            elif fit > delta_score:
                delta_score, delta_pos = fit, positions[i].copy()

        # 2) Update each wolf’s position
        for i in range(num_wolves):
            for d in range(dim):
                # coefficients for Alpha
                r1, r2 = np.random.rand(), np.random.rand()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha_pos[d] - positions[i, d])
                X1 = alpha_pos[d] - A1 * D_alpha

                # Beta
                r1, r2 = np.random.rand(), np.random.rand()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta_pos[d] - positions[i, d])
                X2 = beta_pos[d] - A2 * D_beta

                # Delta
                r1, r2 = np.random.rand(), np.random.rand()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta_pos[d] - positions[i, d])
                X3 = delta_pos[d] - A3 * D_delta

                # New position is average of the three
                positions[i, d] = (X1 + X2 + X3) / 3

    # After all iterations, set the bot to the best hyperparams found
    # Clip & cast alpha_pos one last time
    best = []
    for d in range(dim):
        col = bot.bounds[d]
        val = alpha_pos[d]
        val = max(min(val, max(col)), min(col))
        if all(isinstance(x, int) for x in col):
            val = int(round(val))
        best.append(val)
    bot.hyperparams = best

    return alpha_score
