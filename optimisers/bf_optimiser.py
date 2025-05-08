import numpy as np
import random

# Initialises the population of bacteria to random positions
def initialise_population(bounds, bacterium):
    colony = []

    # Loop for each bacterium
    for _ in range(bacterium):
        position = []
        for bound in bounds:
            if isinstance(bound, tuple):  # Continuous
                val = np.random.uniform(bound[0], bound[1])
            elif isinstance(bound, list):  # Discrete
                val = np.random.choice(bound)
            else:
                raise ValueError("Unsupported bound type")
            position.append(val)
        colony.append(position)

    return np.array(colony)

# Function to calculate the amount of swarming effect on a bacterium
def swarming_effect(current_position, all_positions, d_attract=0.1, w_attract=0.2, h_repel=0.1, w_repel=10):
    effect = 0
    for other in all_positions:
        dist_sq = np.sum((np.array(current_position) - np.array(other)) ** 2)
        attract = -d_attract * np.exp(-w_attract * dist_sq)
        repel = h_repel * np.exp(-w_repel * dist_sq)
        effect += attract + repel
    return effect

# Function to take a chemotactic step for a bacterium
def chemotactic_step(bounds, colony, bacterium, run=False, last_direction=None, tumble_chance=0.2, step_percentage=0.01):
    new_bacterium = []
    direction_used = []

    effect = swarming_effect(bacterium, colony)
    if last_direction is not None:
        last_direction = [d + effect for d in last_direction] # Adding the swarming effect to last direction vector

    tumble = not run or random.random() < tumble_chance  # Chance to tumble regardless if fitness improved (increasing exploitation chance)

    for i, param in enumerate(bacterium):
        bound = bounds[i]

        if isinstance(bound, tuple):  # Continuous
            lower, upper = bound
            step_size = (upper - lower) * step_percentage

            delta = np.random.uniform(-step_size, step_size) #+ effect

            if not tumble and last_direction is not None:
                delta = last_direction[i]

            new_param = param + delta
            new_param = max(lower, min(upper, new_param))

        elif isinstance(bound, list):  # Discrete
            choices = bound
            idx = choices.index(int(round(param)))

            move = int(np.random.choice([-1, 0, 1]) )#+ int(round(effect)))

            if not tumble and last_direction is not None:
                move = int(round(last_direction[i]))
            # Ensure the index stays within bounds
            new_idx = max(0, min(len(choices) - 1, idx + move))
            new_param = choices[new_idx]

            # For reuse, store relative index movement
            move = new_idx - idx
            delta = move

        else:
            raise ValueError("Unsupported bound type")

        new_bacterium.append(new_param)
        direction_used.append(delta)

    return new_bacterium, direction_used

def reproduce(colony, data, bot, step_percentage=0.01):
    fitnesses = []

    # Evaluate the fitness for each bacterium and store it along with the bacterium
    for bacterium in colony:
        bot.hyperparams = bacterium
        fitness = bot.fitness(data)  # Get the fitness of the current bacterium
        fitnesses.append((fitness, bacterium))  # Store as tuple (fitness, bacterium)

    # Sort bacteria by fitness (highest fitness first)
    fitnesses.sort(key=lambda x: x[0], reverse=True)

    # Take the healthiest half
    num = len(fitnesses) // 2
    fittest = fitnesses[:num]

    # Create new colony (only parameter vectors, no fitness)
    new_colony = []

    for fitness, bacterium in fittest:
        # Keep parents same (no change)
        new_colony.append(bacterium)

        # Create slightly tweaked offspring
        offspring, _ = chemotactic_step(bot.bounds, colony, bacterium, step_percentage=step_percentage, run=False)
        new_colony.append(offspring)

    return new_colony

def bf_optimiser(bot, data, population=20, elim_disp_events=5, reproduction_events=5, chemotactic_steps=50):
    """
    Optimizes the hyperparameters of a bot instance using Bacterial Foraging Optimisation Techniques.

    Parameters:
        bot (bot): An instance of the bot class.
        data (pd.DataFrame): The dataset containing price data.
        population (int): The population size of the "bacterial colony".
        elim_disp_events (int): The number of elimination-dispersal events.
        reproduction_events (int): The number of reproduction events.
        chemotactic_steps (int): The number of steps taken between reproduction events.


    Returns:
        list: The best hyperparameters found during optimization.
    """

    colony = initialise_population(bot.bounds, population)
    colony_best = (-np.inf, None)

    # Loop for each bacterium
    for _ in range(elim_disp_events):
        for _ in range(reproduction_events):
            for _ in range(chemotactic_steps):
                fit = -np.inf  # Reset fitness for each step
                best = (-np.inf, None)  # Reset best for each step
                for i in range(population):
                    previous_fit = fit
                    bacterium, directions = colony[i], None
                    bot.hyperparams = bacterium

                    fit = bot.fitness(data)
                    run = False if previous_fit > fit else True

                    if fit > best[0]: # Track the step's best fitness
                        best = (fit, bacterium)
                    bacterium, directions = chemotactic_step(bounds=bot.bounds, colony=colony, bacterium=bacterium, run=run, last_direction=directions)

                    colony[i] = bacterium

                colony_best = best if best[0] > colony_best[0] else colony_best

            # Reproduction event occurs
            colony = reproduce(colony, data, bot, step_percentage=0.01)

        # Elimination-dispersal event occurs
        for i in range(population):
            if np.random.random() < 0.25:  # Probability of dispersal
                colony[i] = initialise_population(bot.bounds, 1)[0]

    # Final evaluation of the colony
    for i in range(population):
        bot.hyperparams = colony[i]
        if bot.fitness(data) > colony_best[0]:
            colony_best = (bot.fitness(data), colony[i])
    return colony_best