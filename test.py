from pathlib import Path

# Define the sample project structure
structure = [
    "ai-trading-bot/data",
    "ai-trading-bot/filters",
    "ai-trading-bot/signals",
    "ai-trading-bot/bot",
    "ai-trading-bot/optimisers",
    "ai-trading-bot/experiments",
    "ai-trading-bot/utils",
]

# Create directories
for path in structure:
    Path(path).mkdir(parents=True, exist_ok=True)

# Create initial Python files
files = {
    "ai-trading-bot/filters/sma.py": """import numpy as np

def sma_filter(window):
    return np.ones(window) / window
""",
    "ai-trading-bot/filters/lma.py": """import numpy as np

def lma_filter(window):
    weights = np.arange(1, window + 1)
    return weights / weights.sum()
""",
    "ai-trading-bot/filters/ema.py": """import numpy as np

def ema_filter(window, alpha):
    weights = [(1 - alpha) ** k for k in range(window)]
    weights = np.array(weights)[::-1]  # most recent weight last
    return alpha * weights / sum(weights)
""",
    "ai-trading-bot/filters/custom_filters.py": """# Define any additional or hybrid filters here
""",
    "ai-trading-bot/signals/crossover.py": """import numpy as np

def generate_signals(short_ma, long_ma):
    signal = np.where(short_ma > long_ma, 1, 0)
    position = np.diff(signal, prepend=0)
    return position
""",
    "ai-trading-bot/signals/macd.py": """# Optional: MACD signal generation
""",
    "ai-trading-bot/bot/trader.py": """def simulate_trades(prices, signals, fee=0.03, initial_cash=1000):
    cash = initial_cash
    btc = 0
    for price, signal in zip(prices, signals):
        if signal == 1 and cash > 0:
            btc = (cash * (1 - fee)) / price
            cash = 0
        elif signal == -1 and btc > 0:
            cash = btc * price * (1 - fee)
            btc = 0
    if btc > 0:
        cash = btc * prices[-1] * (1 - fee)
    return cash
""",
    "ai-trading-bot/bot/evaluation.py": """from .trader import simulate_trades

def evaluate(prices, signals):
    return simulate_trades(prices, signals)
""",
    "ai-trading-bot/optimisers/genetic.py": """# Genetic algorithm implementation goes here
""",
    "ai-trading-bot/optimisers/pso.py": """# Particle Swarm Optimization implementation goes here
""",
    "ai-trading-bot/experiments/run_optimisation.py": """# Optimisation loop and parameter tuning
""",
    "ai-trading-bot/experiments/test_final_bot.py": """# Evaluate the final bot on test data
""",
    "ai-trading-bot/utils/data_loader.py": """import pandas as pd

def load_price_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    return df['Close']
""",
    "ai-trading-bot/README.md": "# AI Trading Bot\n\nInstructions to run the bot and optimiser.",
    "ai-trading-bot/requirements.txt": "numpy\npandas\nmatplotlib\n"
}

# Create the files with initial content
for file_path, content in files.items():
    Path(file_path).write_text(content)

"Project structure and files created successfully."
