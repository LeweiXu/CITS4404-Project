import os
import importlib
from utils.data_loader import read_csv
from config import *
from utils.plots import plot

# Dynamically import all bots from the bots/ folder
def import_bots():
    bots_path = os.path.join(os.path.dirname(__file__), 'bots')
    bots = {}
    for file in os.listdir(bots_path):
        if file.endswith('.py') and file != '__init__.py':
            bot_name = file[:-3]  # Remove the '.py' extension
            try:
                # Import the bot module
                module = importlib.import_module(f'bots.{bot_name}')
                # Check if the module has an instance of a bot
                if hasattr(module, f'{bot_name}_instance'):
                    bots[bot_name] = getattr(module, f'{bot_name}_instance')
            except Exception as e:
                print(f"Error importing {bot_name}: {e}")
    return bots

def test_bots(dataset_path):
    """
    Tests all bots against the given dataset.

    Parameters:
        dataset_path (str): Path to the dataset file.
        granularity (str): The granularity of the dataset (e.g., 'daily', 'hourly').

    Returns:
        dict: A dictionary with bot names as keys and their final cash values as values.
    """
    results = {}
    bots = import_bots()  # Import all bots
    data = read_csv(dataset_path)

    for bot_name, bot_instance in bots.items():
        try:
            print(f"Testing {bot_name}...")
            signals = bot_instance.generate_signals(data)
            plot(data, signals, plot_name=f"{bot_name}_{dataset_path.split('/')[-1].split('.')[0]}")
            results[bot_name] = bot_instance.fitness(data)
        except Exception as e:
            print(f"Error testing {bot_name}: {e}")

    sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    return sorted_results

if __name__ == "__main__":
    # Paths to the datasets
    dataset_2020_daily = DATASET_2020_DAILY_PATH
    dataset_2021_daily = DATASET_2021_DAILY_PATH
    dataset_2020_hourly = DATASET_2020_HOURLY_PATH
    dataset_2021_hourly = DATASET_2021_HOURLY_PATH

    print("Testing against the 2020 daily dataset...")
    results_2020_daily = test_bots(dataset_2020_daily)
    print("\nTesting against the 2021 daily dataset...")
    results_2021_daily = test_bots(dataset_2021_daily)

    print("\nTesting against the 2020 hourly dataset...")
    results_2020_hourly = test_bots(dataset_2020_hourly)
    print("\nTesting against the 2021 hourly dataset...")
    results_2021_hourly = test_bots(dataset_2021_hourly)

    print("\nAll trading bots start with $1000 cash and all transactions incur a 3% fee")
    print("Each bot begins trading on the first day of the year and the balance after 365 days of trading is the score")
    # Combine results into a leaderboard format
    print("Leaderboard:")
    print(f"{'Rank':<5} {'Bot':<20} {'2020 Daily ($)':<15} {'2021 Daily ($)':<15} {'2020 Hourly ($)':<15} {'2021 Hourly ($)':<15} {'Average ($)':<15}")
    print("-" * 100)

    # Create a combined list of bots from all datasets
    all_bots = set(results_2020_daily.keys()).union(
        results_2021_daily.keys(),
        results_2020_hourly.keys(),
        results_2021_hourly.keys()
    )

    # Sort bots by the average of the 4 results
    sorted_bots = sorted(
        all_bots,
        key=lambda bot: (
            (
                results_2020_daily.get(bot, 0) +
                results_2021_daily.get(bot, 0) +
                results_2020_hourly.get(bot, 0) +
                results_2021_hourly.get(bot, 0)
            ) / 4
        ),
        reverse=True
    )

    for rank, bot in enumerate(sorted_bots, start=1):
        cash_2020_daily = results_2020_daily.get(bot, 0)
        cash_2021_daily = results_2021_daily.get(bot, 0)
        cash_2020_hourly = results_2020_hourly.get(bot, 0)
        cash_2021_hourly = results_2021_hourly.get(bot, 0)
        average = (
            cash_2020_daily +
            cash_2021_daily +
            cash_2020_hourly +
            cash_2021_hourly
        ) / 4
        print(f"{rank:<5} {bot:<20} {cash_2020_daily:<15.2f} {cash_2021_daily:<15.2f} {cash_2020_hourly:<15.2f} {cash_2021_hourly:<15.2f} {average:<15.2f}")