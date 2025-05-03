import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
#----------------Bots----------------
from bots.bollinger_bot import bollinger_bot
from bots.custom_wma_bot import custom_wma_bot
from bots.gwo_bot import gwo_bot
from bots.macd_bot import macd_bot
from bots.simple_bot import simple_bot
from bots.wma_rsi_bot import wma_rsi_bot
#from bots.zero_cross_bot import zero_cross_bot    #bugged
#----------------Optimisers----------------
from optimisers.aco_optimiser import aco_optimiser
from optimisers.bf_optimiser import bf_optimiser
from optimisers.gwo_optimiser import gwo_optimiser
from optimisers.hook_jeeves import hook_jeeves
from optimisers.pso_optimiser import pso_optimiser

data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-12-31")

bot_names = ["Bollinger", "Custom WMA", "GWO", "MACD", "Simple", "WMA RSI"]
bots = [bollinger_bot(), custom_wma_bot(), gwo_bot(), macd_bot(), simple_bot(), wma_rsi_bot()]
collect_bot =  [True, True, True, True, True, True]
plot_bot = [True, True, True, True, True, True]

optimiser_names = ["ACO", "BF", "GWO", "Hook Jeeves", "PSO"]
optimisers = [aco_optimiser, bf_optimiser, gwo_optimiser, hook_jeeves, pso_optimiser]
collect_optimiser = [True, True, True, True, True, True]
plot_optimiser = [False, False, True, False, False]

# Collect Data
attempts_per_optimiser = 10
fitness_data = np.zeros([len(bots),len(optimisers),attempts_per_optimiser],float)
for i in range(len(bots)):
    if collect_bot[i] == True:
        for k in range(len(optimisers)):
            if collect_optimiser[k] == True:
                if plot_optimiser[k] == True and plot_bot[i] == True:
                    plt.figure(i)
                    plt.title(bot_names[i])
                for j in range(attempts_per_optimiser):
                    try:
                        history = optimisers[k](bots[i], data, fit_history = True)
                        fitness_data[i][k][j] = history[len(history)-1]
                        if plot_optimiser[k] == True and plot_bot[i] == True:
                            plt.plot(history, color = "blue")
                            print(f"plotted and Computed {bot_names[i]} using {optimiser_names[k]}")
                        else:
                            print(f"computed {bot_names[i]} using {optimiser_names[k]}")
                    except Exception as e:
                        print(f"Error testing: {e}")
                print(f"Completed {optimiser_names[k]}")
            else:
                print(f"Skipped {optimiser_names[k]}")
        print(f"Completed {bot_names[i]}")
    else:
        print(f"Skipped {bot_names[i]}")


plt.figure(7)   

m = len(bots)  # Number of bots
n = len(optimisers)  # Number of algorithms

fig, ax = plt.subplots(figsize=(14, 6))
positions = []
data_to_plot = []
labels = []
colors = []

# Offsets for boxplot positioning
offset = 0.15
group_width = n * offset

# Define a color map with n distinct colors
cmap = cm.get_cmap('tab10', n)  # tab10 has 10 distinct, readable colors

for bot_idx in range(m):
    for algo_idx in range(n):
        pos = bot_idx * (group_width + 0.5) + algo_idx * offset
        positions.append(pos)
        data_to_plot.append(fitness_data[bot_idx, algo_idx])
        labels.append(f"Algorithm {optimiser_names[algo_idx]}\nBOT {bot_names[bot_idx]}")
        colors.append(cmap(algo_idx))  # Assign consistent color for each algorithm

# Create boxplots
box = ax.boxplot(data_to_plot, positions=positions, vert=True, patch_artist=True, widths = 0.1)

# Apply colors to boxes
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    
# Add x-axis tick labels for each boxplot
ax.set_xticks(positions)
ax.set_xticklabels(labels, rotation=90, ha='center')

# Label y-axis
ax.set_ylabel("Fitness")

plt.tight_layout()
plt.show()