def simulate_trades(prices, signals, fee=0.03, initial_cash=1000, signal_threshold=0.5):
    cash = initial_cash
    btc = 0
    for price, signal in zip(prices, signals):
        if signal > signal_threshold and cash > 0: # Buy signal
            btc = (cash * (1 - fee)) / price
            cash = 0
        elif signal < -signal_threshold and btc > 0: # Sell signal
            cash = btc * price * (1 - fee)
            btc = 0
    if btc > 0:
        cash = btc * prices[-1] * (1 - fee)
    return cash
