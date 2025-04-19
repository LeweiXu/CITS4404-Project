def rsi(prices, period=14):
    # Calculate the difference between consecutive prices
    deltas = np.diff(prices)

    # Use the first 'period' deltas to initialize RSI
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period  # Average gains
    down = -seed[seed < 0].sum() / period  # Average losses
    rs = up / down if down != 0 else 0
    rsi_values = [100. - 100. / (1. + rs)]  # Initial RSI value

    # Continue calculating RSI values using the exponential smoothing formula
    for i in range(period, len(deltas)):
        delta = deltas[i]
        if delta >= 0:
            up_val = delta
            down_val = 0.
        else:
            up_val = 0.
            down_val = -delta

        up = (up * (period - 1) + up_val) / period
        down = (down * (period - 1) + down_val) / period

        rs = up / down if down != 0 else 0
        rsi_values.append(100. - 100. / (1. + rs))

    # Pad the beginning with zeros to maintain the same length
    return np.array([0] * period + rsi_values)


import numpy as np
from filters.wma import wma, sma_filter
# from utils.rsi import rsi
from bots.bot_base import bot


class wma_rsi_bot(bot):
    def __init__(self):
        self.hyperparams = []
        # Define the bounds for each hyperparameter:
        # p1: Fast WMA period
        # p2: Slow WMA period
        # rsi_period: RSI calculation period
        # rsi_buy_th: RSI threshold to trigger a buy signal
        # rsi_sell_th: RSI threshold to trigger a sell signal
        self.bounds = [
            [i for i in range(5, 51)],  # p1: WMA fast
            [i for i in range(10, 101)],  # p2: WMA slow
            [i for i in range(7, 22)],  # RSI period
            [i for i in range(30, 51)],  # RSI buy threshold
            [i for i in range(50, 71)]  # RSI sell threshold
        ]

    def generate_signals(self, data):
        prices = data['close'].values
        p1, p2, rsi_period, rsi_buy_th, rsi_sell_th = map(int, self.hyperparams)

        # Calculate the fast and slow WMA lines
        sma_fast = wma(prices, p1, sma_filter(p1))
        sma_slow = wma(prices, p2, sma_filter(p2))

        # Compute RSI values for the price series
        rsi_vals = rsi(prices, rsi_period)

        signals = []
        for i in range(len(prices)):
            # Skip early data points where indicators are not valid yet
            if i < max(p1, p2, rsi_period):
                signals.append(0)
                continue

            # Entry condition for a buy signal
            bullish = sma_fast[i] > sma_slow[i] and rsi_vals[i] < rsi_buy_th

            # Entry condition for a sell signal
            bearish = sma_fast[i] < sma_slow[i] and rsi_vals[i] > rsi_sell_th

            if bullish:
                signals.append(1)
            elif bearish:
                signals.append(-1)
            else:
                signals.append(0)

        return np.array(signals)
