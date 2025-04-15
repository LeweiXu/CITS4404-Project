import numpy as np
from utils.data_loader import read_csv
from bot.trader import simulate_trades
from filters.wma import wma, sma_filter
from config import DATASET_PATH

def test_trading_bot(file_path):
    """
    Naive trading bot using a 10-day and 40-day SMA crossover strategy.
    Uses default of 1 year of trading (in 2017) and 3% fee.

    Parameters:
        file_path (str): Path to the CSV file containing price data.

    Returns:
        float: Final cash after simulating trades.
    """
    # Load the data
    data = read_csv(file_path, columns=['date', 'close'])
    prices = data['close'].values

    # Calculate 10-day and 40-day SMA (with padding)
    sma_10 = wma(prices, 10, sma_filter(10))
    sma_40 = wma(prices, 40, sma_filter(40))

    # debugging output (check if padding worked)
    print(len(prices), len(sma_10), len(sma_40))
    
    # if sma_10 > sma_40, buy, otherwise sell
    signal = np.where(sma_10 > sma_40, 1, 0)
    signals = np.diff(signal, prepend=0)

    # Simulate trades
    final_cash = simulate_trades(prices, signals)

    return final_cash

if __name__ == "__main__":
    file_path = DATASET_PATH
    final_cash = test_trading_bot(file_path)
    print(f"Final cash after trading: ${final_cash:.2f}")