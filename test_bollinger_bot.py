from utils.plots import plot
from utils.data_loader import read_csv

def test_macd_bot_with_generated_data():
    """
    Generate 4 test datasets and test them against the MACD bot.
    """
    from bots.bollinger_bot import bollinger_bot
    default_bollinger_bot = bollinger_bot()
    default_bollinger_bot.hyperparams = [20, 2] # Traditional Bollinger Bands

    # Generate 4 datasets
    datasets = [
        read_csv("data/BTC-Daily-2020.csv", start_date="2020-01-01", end_date="2020-12-31"),
        read_csv("data/BTC-Daily-2021.csv", start_date="2021-01-01", end_date="2021-12-31")
    ]

    for i, data in enumerate(datasets, start=1):
        try:
            print(f"Testing Bollinger bot on generated dataset {i}...")
            signals = default_bollinger_bot.generate_signals(data)
            plot(
                data,
                signals,
                plot_name=f"bollinger_bot_BTC-Daily_default_{i}",
            )

        except Exception as e:
            print(f"Error testing MACD bot on generated dataset {i}: {e}")

if __name__ == "__main__":
    test_macd_bot_with_generated_data()