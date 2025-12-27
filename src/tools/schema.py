from . import load_dataset
from typing import Dict, List, Any


def analyze_schema(dataset_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Analyze the schema of a dataset, returning information about each column.
    """
    try:
        df = load_dataset(dataset_id)
        return {
            "columns": [
                {
                    "name": c,
                    "dtype": str(df[c].dtype),
                    "missing": int(df[c].isna().sum())
                }
                for c in df.columns
            ]
        }
    except Exception as e:
        raise RuntimeError(
            f"Failed to analyze schema for dataset '{dataset_id}': {str(e)}")
