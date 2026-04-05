import pandas as pd


def get_last_rows(dataset: str, n_rows: int = 5) -> str:
    """
    Get the last n rows for a given dataset.

    Args:
        dataset: the name of the dataset
        n_rows: the numbers of rows

    Returns:
        A string containing the last n rows in markdown format
    """
    if not dataset.endswith(".csv"):
        dataset = dataset + ".csv"

    try:
        df = pd.read_csv("datasets/" + dataset)
        # We MUST return the string, not print it!
        # .to_markdown() creates a clean table for the LLM to read
        return df.tail(n_rows).to_markdown()
    except Exception as e:
        return f"Error reading file: {str(e)}"


available_tools = [get_last_rows]
