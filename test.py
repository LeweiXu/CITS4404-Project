import matplotlib.pyplot as plt
import numpy as np
from bots.example_bot import *
from trader import simulate_trades
from utils.data_loader import read_csv
from config import DATASET_2020_HOURLY_PATH, DATASET_2020_DAILY_PATH

# Load the data
data = read_csv(DATASET_2020_DAILY_PATH, start_date="2020-03-01", end_date="2020-03-30")
signals = generate_signals(data)

# Simulate trades and print final cash
final_cash = simulate_trades(data['close'].values, signals)
print(f"Final cash: ${final_cash:.2f}")

# Plot 1: Closing prices with buy and sell signals
plt.figure(figsize=(12, 6))
plt.plot(data['close'].values, label='Closing Prices', color='blue', alpha=0.7)
buy_signals = np.where(signals == 1)[0]
plt.scatter(buy_signals, data['close'].values[buy_signals], label='Buy Signal', color='green', marker='^', alpha=1)
sell_signals = np.where(signals == -1)[0]
plt.scatter(sell_signals, data['close'].values[sell_signals], label='Sell Signal', color='red', marker='v', alpha=1)
plt.title('Closing Prices with Buy and Sell Signals')
plt.xlabel('Time (Index)')
plt.ylabel('Closing Price')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("signals_plot.png")
print("Plot saved as 'signals_plot.png'")

# Plot 2: Bar plot for buy and sell signals
plt.figure(figsize=(12, 6))
bar_colors = ['green' if signals[i] == 1 else 'red' for i in range(len(signals)) if signals[i] != 0]
bar_positions = [i for i in range(len(signals)) if signals[i] != 0]
bar_heights = [data['close'].values[i] for i in bar_positions]

plt.bar(bar_positions, bar_heights, color=bar_colors, alpha=0.7, width=5)
plt.title('Buy and Sell Signals (Bar Plot)')
plt.xlabel('Time (Index)')
plt.ylabel('Closing Price')
plt.grid(alpha=0.3)
plt.savefig("signals_bar_plot.png")
print("Bar plot saved as 'signals_bar_plot.png'")

