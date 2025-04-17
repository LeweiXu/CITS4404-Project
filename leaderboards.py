import os
import importlib
from utils.data_loader import read_csv
from config import *
from utils.trader import simulate_trades

def test_bots(dataset_path):
    """
    Tests all optimization algorithms in the 'optimisers' folder against the given dataset.

    Parameters:
        dataset_path (str): Path to the dataset file.

    Returns:
        dict: A dictionary with optimiser names as keys and their final cash values as values.
    """
    results = {}
    optimisers_path = os.path.join(os.path.dirname(__file__), 'bots')
    data = read_csv(dataset_path)

    # Iterate through all Python files in the 'bots' folder
    for file in os.listdir(optimisers_path):
        if file.endswith('.py') and file != '__init__.py':
            optimiser_name = file[:-3]  # Remove the '.py' extension
            try:
                # Dynamically import the optimiser module
                module = importlib.import_module(f'bots.{optimiser_name}')
                
                # Check if the module has a 'generate_signals' function
                if hasattr(module, 'generate_signals'):
                    print(f"Testing {optimiser_name}...")
                    signals = module.generate_signals(data)
                    results[optimiser_name] = simulate_trades(data['close'].values, signals)
                else:
                    print(f"Skipping {optimiser_name}: 'generate_signals' function not found.")
            except Exception as e:
                print(f"Error testing {optimiser_name}: {e}")

    sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    return sorted_results

if __name__ == "__main__":
    # Paths to the datasets
    dataset_2020_daily = DATASET_2020_DAILY_PATH
    dataset_2021_daily = DATASET_2021_DAILY_PATH
    dataset_2020_hourly = DATASET_2020_HOURLY_PATH
    dataset_2021_hourly = DATASET_2021_HOURLY_PATH
    dataset_2020_minute = DATASET_2020_MINUTE_PATH
    dataset_2021_minute = DATASET_2021_MINUTE_PATH

    print("Testing against the 2020 daily dataset...")
    results_2020_daily = test_bots(dataset_2020_daily)
    print("\nTesting against the 2021 daily dataset...")
    results_2021_daily = test_bots(dataset_2021_daily)

    print("\nTesting against the 2020 hourly dataset...")
    results_2020_hourly = test_bots(dataset_2020_hourly)
    print("\nTesting against the 2021 hourly dataset...")
    results_2021_hourly = test_bots(dataset_2021_hourly)

    print("\nTesting against the 2020 minute dataset...")
    results_2020_minute = test_bots(dataset_2020_minute)
    print("\nTesting against the 2021 minute dataset...")
    results_2021_minute = test_bots(dataset_2021_minute)

    print("\nAll trading bots start with $1000 cash and all transactions incur a 3% fee")
    print("Each bot begins trading on the first day of the year and the balance after 365 days of trading is the score")
    # Combine results into a leaderboard format
    print("Leaderboard:")
    print(f"{'Rank':<5} {'Bot':<20} {'2020 Daily ($)':<15} {'2021 Daily ($)':<15} {'2020 Hourly ($)':<15} {'2021 Hourly ($)':<15} {'2020 Minute ($)':<15} {'2021 Minute ($)':<15} {'Average ($)':<15}")
    print("-" * 120)

    # Create a combined list of bots from all datasets
    all_bots = set(results_2020_daily.keys()).union(
        results_2021_daily.keys(),
        results_2020_hourly.keys(),
        results_2021_hourly.keys(),
        results_2020_minute.keys(),
        results_2021_minute.keys()
    )

    # Sort bots by the average of the 6 results
    sorted_bots = sorted(
        all_bots,
        key=lambda bot: (
            (
                results_2020_daily.get(bot, 0) +
                results_2021_daily.get(bot, 0) +
                results_2020_hourly.get(bot, 0) +
                results_2021_hourly.get(bot, 0) +
                results_2020_minute.get(bot, 0) +
                results_2021_minute.get(bot, 0)
            ) / 6
        ),
        reverse=True
    )

    for rank, bot in enumerate(sorted_bots, start=1):
        cash_2020_daily = results_2020_daily.get(bot, 0)
        cash_2021_daily = results_2021_daily.get(bot, 0)
        cash_2020_hourly = results_2020_hourly.get(bot, 0)
        cash_2021_hourly = results_2021_hourly.get(bot, 0)
        cash_2020_minute = results_2020_minute.get(bot, 0)
        cash_2021_minute = results_2021_minute.get(bot, 0)
        average = (
            cash_2020_daily +
            cash_2021_daily +
            cash_2020_hourly +
            cash_2021_hourly +
            cash_2020_minute +
            cash_2021_minute
        ) / 6
        print(f"{rank:<5} {bot:<20} {cash_2020_daily:<15.2f} {cash_2021_daily:<15.2f} {cash_2020_hourly:<15.2f} {cash_2021_hourly:<15.2f} {cash_2020_minute:<15.2f} {cash_2021_minute:<15.2f} {average:<15.2f}")