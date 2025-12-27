import pandas as pd
from . import load_dataset, DATASET_SCHEMA
from ..tools_registry import register_tool
from typing import Dict, Any


def compute_basic_stats(dataset_id: str) -> Dict[str, Any]:
    """
    Compute basic statistics for a dataset, including row count, column count, and numeric summaries.
    """
    try:
        df = load_dataset(dataset_id)  # read-only
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_summary": df.describe().to_dict() if not df.empty else {}
        }
    except Exception as e:
        raise RuntimeError(
            f"Failed to compute basic stats for dataset '{dataset_id}': {str(e)}")


# Register the tool
register_tool(
    name="compute_basic_stats",
    description="Compute basic statistics for a dataset, including number of rows, columns, and descriptive statistics for numeric columns.",
    schema=DATASET_SCHEMA,
    fn=compute_basic_stats
)
