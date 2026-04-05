import pandas as pd


def get_last_rows(dataset: str) -> str:
    """
   Get the last 5 rows for a given dataset.

   Args:
     dataset: the name of the dataset

   Returns:
     A string printing the last 5 rows
   """
    if (not dataset.endswith(".csv")):
        dataset = dataset + ".csv"
    df = pd.read_csv("datasets/" + dataset)
    print(df.tail())


available_tools = [get_last_rows]
