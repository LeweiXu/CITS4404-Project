class bot:
    def __init__(self):
        pass

    def fitness(self, data, fee=0.03, initial_cash=1000):
        signals = self.generate_signals(data)
        prices = data['close'].values
        cash = initial_cash
        btc = 0
        for price, signal in zip(prices, signals):
            # Will only buy/sell if cash/btc is available (> 0)
            if signal == 1 and cash > 0: # Buy signal
                btc = (cash * (1 - fee)) / price
                cash = 0
            elif signal == -1 and btc > 0: # Sell signal
                cash = btc * price * (1 - fee)
                btc = 0
        if btc > 0:
            cash = btc * prices[-1] * (1 - fee)
        return cash