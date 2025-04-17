# AKA the fitness evaluation function 

def simulate_trades(prices, signals, fee=0.03, initial_cash=1000):
    """
    Simulates a trading strategy based on price data and trading signals.
    Args:
        prices (list of float): A list of prices for the asset being traded.
        signals (list of float): A list of trading signals corresponding to the prices.
                                 Positive values indicate buy signals, and negative values indicate sell signals.
        signal_threshold (float, optional): The threshold for signals to trigger a buy or sell action.
                                            Default is 0.5.
    Returns:
        float: The final amount of cash after all trades have been executed.
    Notes:
        - If there is any remaining asset at the end of the simulation, it is converted back to cash using the last price.
        - Transaction fees are applied to both buy and sell operations.
        - Do not change fee & initial_cash parameters (these are project requirements).
    """
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