import matplotlib.pyplot as plt
import numpy as np

def plot(data, signals, plot_name="signals_plot"):
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
    plt.savefig(f"plots/{plot_name}.png")
    print(f"Plot saved as 'plots/{plot_name}.png'")

    # # Plot 2: Bar plot for buy and sell signals
    # plt.figure(figsize=(12, 6))
    # bar_colors = ['green' if signals[i] == 1 else 'red' for i in range(len(signals)) if signals[i] != 0]
    # bar_positions = [i for i in range(len(signals)) if signals[i] != 0]
    # bar_heights = [data['close'].values[i] for i in bar_positions]
    # plt.bar(bar_positions, bar_heights, color=bar_colors, alpha=0.7, width=5)
    # plt.title('Buy and Sell Signals (Bar Plot)')
    # plt.xlabel('Time (Index)')
    # plt.ylabel('Closing Price')
    # plt.grid(alpha=0.3)
    # plt.savefig("plots/signals_bar_plot.png")
    # print("Bar plot saved as 'signals_bar_plot.png'")

def plot_macd_with_signals(data, macd_line, signal_line, signals, plot_name="macd_with_signals"):
    """
    Plot the MACD line, Signal line, prices, and buy/sell signals on the same graph.

    Parameters:
        data (pd.DataFrame): The dataset containing price data.
        macd_line (numpy.ndarray): The MACD line (difference between fast and slow EMA).
        signal_line (numpy.ndarray): The Signal line (EMA of the MACD line).
        signals (numpy.ndarray): Array of buy/sell signals (1 for buy, -1 for sell, 0 for hold).
        plot_name (str): The name of the plot file to save.
    """
    prices = data['close'].values
    buy_signals = np.where(signals == 1)[0]
    sell_signals = np.where(signals == -1)[0]

    plt.figure(figsize=(14, 8))

    # Plot the closing prices
    plt.subplot(2, 1, 1)
    plt.plot(prices, label="Closing Prices", color="blue", alpha=0.7)
    plt.scatter(buy_signals, prices[buy_signals], label="Buy Signal", marker="^", color="green", alpha=1)
    plt.scatter(sell_signals, prices[sell_signals], label="Sell Signal", marker="v", color="red", alpha=1)
    plt.title("Closing Prices with Buy/Sell Signals")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(alpha=0.3)

    # Plot the MACD line and Signal line
    plt.subplot(2, 1, 2)
    plt.plot(macd_line, label="MACD Line", color="orange", alpha=0.7)
    plt.plot(signal_line, label="Signal Line", color="purple", alpha=0.7)
    plt.bar(range(len(macd_line)), macd_line - signal_line, label="MACD Histogram", color="gray", alpha=0.5)
    plt.title("MACD Line and Signal Line")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(alpha=0.3)

    # Save the plot
    plt.tight_layout()
    plt.savefig(f"plots/{plot_name}.png")

import matplotlib.pyplot as plt

def plot_macd(prices, macd_line, signal_line, macd_histogram, plot_name="macd_plot"):
    """
    Plot the MACD line, Signal line, MACD histogram, and prices.

    Parameters:
        prices (numpy.ndarray): Array of price values.
        macd_line (numpy.ndarray): The MACD line (difference between fast and slow EMA).
        signal_line (numpy.ndarray): The Signal Line (EMA of the MACD line).
        macd_histogram (numpy.ndarray): The MACD Histogram (MACD line - Signal line).
        plot_name (str): The name of the plot file to save.
    """
    plt.figure(figsize=(14, 8))

    # Plot the prices
    plt.subplot(2, 1, 1)
    plt.plot(prices, label="Prices", color="blue", alpha=0.7)
    plt.title("Prices")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(alpha=0.3)

    # Plot the MACD line, Signal line, and MACD histogram
    plt.subplot(2, 1, 2)
    plt.plot(macd_line, label="MACD Line", color="orange", alpha=0.7)
    plt.plot(signal_line, label="Signal Line", color="purple", alpha=0.7)
    plt.bar(range(len(macd_histogram)), macd_histogram, label="MACD Histogram", color="gray", alpha=0.5)
    plt.title("MACD Line, Signal Line, and Histogram")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(alpha=0.3)

    # Save the plot
    plt.tight_layout()
    plt.savefig(f"plots/{plot_name}.png")
    plt.close()