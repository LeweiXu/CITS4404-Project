import pandas as pd
import numpy as np

def read_csv(file_path, columns=['date', 'close'], start_date=None, end_date=None):
    """
    Reads a CSV file into a pandas DataFrame with 'date' and 'close' columns by default.
    Optionally includes other columns specified by the user. Returns the DataFrame with rows in reverse order.

    Parameters:
        file_path (str): Path to the CSV file.
        columns (list, optional): List of column names to include. Defaults to ['date', 'close'].
        start_date (str, optional): The date (in 'YYYY-MM-DD' format) to start reading the data. Defaults to None (no filtering by start date).
        end_date (str, optional): The date (in 'YYYY-MM-DD' format) to stop reading the data. Defaults to None (no filtering by end date).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the selected columns, with rows in reverse order.
    """
    try:
        df = pd.read_csv(file_path, usecols=columns)
        df = df.iloc[::-1]  # Reverse the order of rows (datasets are reversed)

        if start_date:
            df = df[df['date'] >= start_date]  # Filter rows starting from the specified start date

        if end_date:
            df = df[df['date'] <= end_date]  # Filter rows up to the specified end date

    except ValueError as e:
        raise ValueError(f"Error reading the file. Ensure the specified columns exist in the CSV. {e}")
    
    return df

def generate_test_data():
    """
    Generate a 100-day test dataset with fluctuating BTC/USD prices.

    Returns:
        pd.DataFrame: A DataFrame with one column 'close' containing 100 points of test data.
    """
    np.random.seed(42)  # For reproducibility
    prices = np.cumsum(np.random.randn(100) * 10 + 50000)  # Simulate price fluctuations around $50,000
    dates = pd.date_range(start="2025-01-01", periods=100)
    return pd.DataFrame({"date": dates, "close": prices})