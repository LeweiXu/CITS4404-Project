from utils.data_loader import read_csv
from config import TRAINING_DATASET_PATH
from utils.plots import plot
import numpy as np
data = read_csv(TRAINING_DATASET_PATH, start_date="2015-01-01", end_date="2015-10-31")
signals = np.array([0 for _ in range(len(data))])
plot(data, signals, "test_plot")
print("Plot saved to plots/test_plot.png")