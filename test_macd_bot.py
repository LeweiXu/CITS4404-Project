from utils.plots import plot_macd_with_signals
from utils.data_loader import generate_test_data, read_csv

def test_macd_bot_with_generated_data():
    """
    Generate 4 test datasets and test them against the MACD bot.
    """
    from bots.macd_bot import macd_bot_instance

    # Generate 4 datasets
    datasets = [
        read_csv("data/BTC-Daily-2020.csv", start_date="2020-01-01", end_date="2020-12-31"),
        read_csv("data/BTC-Daily-2021.csv", start_date="2021-01-01", end_date="2021-12-31")
    ]

    for i, data in enumerate(datasets, start=1):
        try:
            print(f"Testing MACD bot on generated dataset {i}...")

            # Generate signals and MACD lines
            signals, macd_line, signal_line = macd_bot_instance.generate_signals(data)
            # Plot the results
            plot_macd_with_signals(
                data,
                macd_line,
                signal_line,
                signals,
                plot_name=f"macd_bot_BTC-Daily-2020_with_signals_aco_{i}"
            )

        except Exception as e:
            print(f"Error testing MACD bot on generated dataset {i}: {e}")

if __name__ == "__main__":
    test_macd_bot_with_generated_data()