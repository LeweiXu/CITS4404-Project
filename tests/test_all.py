import os
import importlib
import numpy as np
from utils.data_loader import read_csv
from config import *
import matplotlib.pyplot as plt

np.random.seed(4404)

def import_classes(folder, base_package):
    """
    Dynamically import classes from Python files in a folder.

    Parameters:
        folder (str): Path to the folder containing the Python files.
        base_package (str): Base package name for imports.

    Returns:
        dict: A dictionary with file names as keys and imported classes as values.
    """
    classes = {}
    for file in os.listdir(folder):
        if file.endswith('.py') and file != '__init__.py':
            class_name = file[:-3]
            try:
                module = importlib.import_module(f'{base_package}.{class_name}')
                if hasattr(module, class_name):
                    classes[class_name] = getattr(module, class_name)
            except Exception as e:
                print(f"Error importing {class_name}: {e}")
    return classes

def save_ranking_graph(data, title, xlabel, ylabel, output_file):
    """
    Save a ranking bar chart to the plots/ folder.

    Parameters:
        data (dict): A dictionary with names as keys and scores as values.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        output_file (str): Path to save the plot.
    """
    names = list(data.keys())
    scores = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.barh(names, scores, color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gca().invert_yaxis()  # Invert y-axis to show the highest rank at the top
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

    print(f"Graph saved as '{output_file}'")

def generate_graphs(results):
    """
    Generate graphs for bot and optimizer rankings.

    Parameters:
        results (dict): The results dictionary from the test_all.py script.
    """
    # Rank bots by average fitness
    bot_averages = {
        bot_name: sum(metrics['average'] for metrics in bot_results.values()) / len(bot_results)
        for bot_name, bot_results in results.items()
    }
    sorted_bots = dict(sorted(bot_averages.items(), key=lambda item: item[1], reverse=True))
    save_ranking_graph(
        sorted_bots,
        title="Ranking of Bots by Average Fitness",
        xlabel="Average Fitness",
        ylabel="Bots",
        output_file="plots/bot_ranking.png"
    )

    # Rank optimizers by average performance
    optimizer_averages = {}
    for bot_results in results.values():
        for optimizer_name, metrics in bot_results.items():
            if optimizer_name not in optimizer_averages:
                optimizer_averages[optimizer_name] = []
            optimizer_averages[optimizer_name].append(metrics['average'])

    optimizer_averages = {
        optimizer_name: sum(averages) / len(averages)
        for optimizer_name, averages in optimizer_averages.items()
    }
    sorted_optimizers = dict(sorted(optimizer_averages.items(), key=lambda item: item[1], reverse=True))
    save_ranking_graph(
        sorted_optimizers,
        title="Ranking of Optimizers by Average Performance",
        xlabel="Average Performance",
        ylabel="Optimizers",
        output_file="plots/optimizer_ranking.png"
    )

def test_bots_and_optimisers(start_date=None, end_date=None):
    bots_folder = os.path.join(os.path.dirname(__file__), 'bots')
    optimisers_folder = os.path.join(os.path.dirname(__file__), 'optimisers')

    bots = import_classes(bots_folder, 'bots')
    optimisers = import_classes(optimisers_folder, 'optimisers')

    training_data = read_csv(TRAINING_DATASET_PATH, start_date=start_date, end_date=end_date)
    dataset_2020 = read_csv(DATASET_2020_DAILY_PATH)
    dataset_2021 = read_csv(DATASET_2021_DAILY_PATH)

    results = {}

    for bot_name, bot_class in bots.items():
        try:
            bot_instance = bot_class()
            results[bot_name] = {}

            for optimiser_name, optimiser_func in optimisers.items():
                try:
                    print(f"Optimizing {bot_name} with {optimiser_name}...")
                    optimiser_func(bot_instance, training_data)

                    fitness_2020 = bot_instance.fitness(dataset_2020)
                    fitness_2021 = bot_instance.fitness(dataset_2021)
                    average_fitness = (fitness_2020 + fitness_2021) / 2

                    results[bot_name][optimiser_name] = {
                        '2020': fitness_2020,
                        '2021': fitness_2021,
                        'average': average_fitness
                    }
                except Exception as e:
                    print(f"Error optimizing {bot_name} with {optimiser_name}: {e}")
        except Exception as e:
            print(f"Error initializing {bot_name}: {e}")

    # Print overall results
    print("\nOverall Results:")
    for bot_name, bot_results in results.items():
        print(f"\n{bot_name}:")
        for optimiser_name, metrics in bot_results.items():
            print(f"  {optimiser_name}: 2020: {metrics['2020']:.2f}, 2021: {metrics['2021']:.2f}, Average: {metrics['average']:.2f}")

    # Rank by bot
    print("\nRanking by Bot:")
    bot_averages = {
        bot_name: sum(metrics['average'] for metrics in bot_results.values()) / len(bot_results)
        for bot_name, bot_results in results.items()
    }
    sorted_bots = sorted(bot_averages.items(), key=lambda item: item[1], reverse=True)
    for rank, (bot_name, avg) in enumerate(sorted_bots, start=1):
        print(f"{rank}. {bot_name}: Average Fitness: {avg:.2f}")

    # Rank by optimiser
    print("\nRanking by optimiser:")
    optimiser_averages = {}
    for bot_results in results.values():
        for optimiser_name, metrics in bot_results.items():
            if optimiser_name not in optimiser_averages:
                optimiser_averages[optimiser_name] = []
            optimiser_averages[optimiser_name].append(metrics['average'])

    optimiser_averages = {
        optimiser_name: sum(averages) / len(averages)
        for optimiser_name, averages in optimiser_averages.items()
    }
    sorted_optimisers = sorted(optimiser_averages.items(), key=lambda item: item[1], reverse=True)
    for rank, (optimiser_name, avg) in enumerate(sorted_optimisers, start=1):
        print(f"{rank}. {optimiser_name}: Average Fitness: {avg:.2f}")

    # Generate and save ranking graphs
    generate_graphs(results)

if __name__ == "__main__":
    # SET START AND END DATES HERE
    # Default is None, which means the entire training dataset will be used
    # "Rocky" dataset is from 2015-01-01 to 2015-10-31
    test_bots_and_optimisers(start_date=None, end_date=None)