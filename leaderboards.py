# Yes most of this code is AI generated
import os
import importlib
from utils.data_loader import read_csv
from config import DATASET_2020_PATH, DATASET_2021_PATH
from trader import simulate_trades

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
                
                # Check if the module has a 'test_trading_bot' function
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
    dataset_2020 = DATASET_2020_PATH
    dataset_2021 = DATASET_2021_PATH

    print("All trading bots start with $1000 cash and all transactions incur a 3% fee")
    print("Testing against the 2020 daily dataset...")
    results_2020 = test_bots(dataset_2020)
    print("\nTesting against the 2021 daily dataset...")
    results_2021 = test_bots(dataset_2021)

    print("\nAll trading bots start with $1000 cash and all transactions incur a 3% fee")
    print("Each bot begins trading on the first day of the year and the balance after 365 days of trading is the score")
    # Combine results into a leaderboard format
    print("Leaderboard:")
    print(f"{'Rank':<5} {'Bot':<20} {'2020 ($)':<15} {'2021 ($)':<15} {'Average ($)':<15}")
    print("-" * 70)

    # Create a combined list of bots from both years
    all_bots = set(results_2020.keys()).union(results_2021.keys())
    sorted_bots = sorted(
        all_bots,
        key=lambda bot: ((results_2020.get(bot, 0) + results_2021.get(bot, 0)) / 2),
        reverse=True
    )

    for rank, bot in enumerate(sorted_bots, start=1):
        cash_2020 = results_2020.get(bot, 0)
        cash_2021 = results_2021.get(bot, 0)
        average = (cash_2020 + cash_2021) / 2
        print(f"{rank:<5} {bot:<20} {cash_2020:<15.2f} {cash_2021:<15.2f} {average:<15.2f}")