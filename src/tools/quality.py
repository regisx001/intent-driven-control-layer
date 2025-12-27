from . import load_dataset, DATASET_SCHEMA
from ..tools_registry import register_tool
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


# Register the tool
register_tool(
    name="detect_missing_values",
    description="Analyze a dataset to detect missing values in each column, returning the proportion of missing values per column.",
    schema=DATASET_SCHEMA,
    fn=detect_missing_values
)
