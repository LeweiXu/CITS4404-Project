import pandas as pd

def read_csv(file_path, columns=['date', 'close'], range=365):
    """
    Reads a CSV file into a pandas DataFrame with 'date' and 'close' columns by default.
    Optionally includes other columns specified by the user. Returns the DataFrame with rows in reverse order.

    Parameters:
        file_path (str): Path to the CSV file.
        columns (list, optional): List of column names to include. Defaults to ['date', 'close'].
        range (int, optional): Number of rows (days) to read after reversing the DataFrame. Defaults to None (all rows).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the selected columns, with rows in reverse order.
    """
    try:
        df = pd.read_csv(file_path, usecols=columns)
        df = df.iloc[::-1]  # Reverse the order of rows (datasets are reversed)
        df = df.head(range)  # Select the specified number of rows
        
    except ValueError as e:
        raise ValueError(f"Error reading the file. Ensure the specified columns exist in the CSV. {e}")
    
    return df