from utils.plots import plot_macd_with_signals
from utils.data_loader import generate_test_data, read_csv
from filters.macd import macd
import numpy as np

def generate_signals(data, hyperparams):
    fast_window, slow_window, signal_window = map(int, hyperparams)

    prices = data["close"].values

    macd_line, signal_line, _ = macd(prices, fast_window, slow_window, signal_window)

    signals = np.zeros_like(macd_line)

    buy_signals = (macd_line[1:] > signal_line[1:]) & (macd_line[:-1] <= signal_line[:-1])
    signals[1:][buy_signals] = 1

    sell_signals = (macd_line[1:] < signal_line[1:]) & (macd_line[:-1] >= signal_line[:-1])
    signals[1:][sell_signals] = -1

    return signals, macd_line, signal_line

def test_macd_bot_with_aco_params():
    """
    Generate 4 test datasets and test them against the MACD bot.
    """

    # Generate 4 datasets
    datasets = [
        read_csv("data/BTC-Daily-2020.csv", start_date="2020-01-01", end_date="2020-12-31"),
        read_csv("data/BTC-Daily-2021.csv", start_date="2021-01-01", end_date="2021-12-31")
    ]
    for i, data in enumerate(datasets, start=1):
        try:
            print(f"Testing MACD bot on generated dataset {i}...")

            # Generate signals and MACD lines
            signals, macd_line, signal_line = generate_signals(data, [125, 192, 140])
            # Plot the results
            plot_macd_with_signals(
                data,
                macd_line,
                signal_line,
                signals,
                plot_name=f"macd_bot_BTC-Daily-with_signals_aco_202{i-1}"
            )
            print(f"Plot saved to plots/macd_bot_BTC-Daily-with_signals_aco_202{i-1}.png")
        except Exception as e:
            print(f"Error testing MACD bot on generated dataset {i}: {e}")

def test_macd_bot_with_default_params():
    """
    Generate 4 test datasets and test them against the MACD bot.
    """

    # Generate 4 datasets
    datasets = [
        read_csv("data/BTC-Daily-2020.csv", start_date="2020-01-01", end_date="2020-12-31"),
        read_csv("data/BTC-Daily-2021.csv", start_date="2021-01-01", end_date="2021-12-31")
    ]
    for i, data in enumerate(datasets, start=1):
        try:
            print(f"Testing MACD bot on generated dataset {i}...")

            # Generate signals and MACD lines
            signals, macd_line, signal_line = generate_signals(data, [12, 26, 9])
            # Plot the results
            plot_macd_with_signals(
                data,
                macd_line,
                signal_line,
                signals,
                plot_name=f"macd_bot_BTC-Daily-with_signals_default_202{i-1}"
            )
            print(f"Plot saved to plots/macd_bot_BTC-Daily-with_signals_default_202{i-1}.png")
        except Exception as e:
            print(f"Error testing MACD bot on generated dataset {i}: {e}")

if __name__ == "__main__":
    test_macd_bot_with_aco_params()
    test_macd_bot_with_default_params()