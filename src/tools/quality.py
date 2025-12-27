from . import load_dataset
from typing import Dict


def detect_missing_values(dataset_id: str) -> Dict[str, float]:
    """
    Detect missing values in each column of the dataset.
    Returns a dictionary with column names as keys and missing value ratios as values.
    """
    try:
        df = load_dataset(dataset_id)
        return {
            col: float(df[col].isna().mean())
            for col in df.columns
        }
    except Exception as e:
        raise RuntimeError(
            f"Failed to detect missing values for dataset '{dataset_id}': {str(e)}")
