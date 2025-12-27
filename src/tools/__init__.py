from . import quality, schema, stats
import pandas as pd
import os
from typing import Dict, Any
from ..tools_registry import register_tool


def load_dataset(dataset_id: str) -> pd.DataFrame:
    """
    Load a dataset by ID. Assumes datasets are stored as CSV files in a 'data' directory.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    os.makedirs(data_dir, exist_ok=True)  # Ensure data directory exists
    file_path = os.path.join(data_dir, f"{dataset_id}.csv")
    if not os.path.exists(file_path):
        raise ValueError(f"Dataset '{dataset_id}' not found at {file_path}")
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load dataset '{dataset_id}': {str(e)}")


# Common schema for dataset_id parameter
DATASET_SCHEMA = {
    "type": "object",
    "properties": {
        "dataset_id": {
            "type": "string",
            "description": "The unique identifier of the dataset to analyze"
        }
    },
    "required": ["dataset_id"]
}

# Import the tool modules to register them


def load_dataset(dataset_id: str) -> pd.DataFrame:
    """
    Load a dataset by ID. Assumes datasets are stored as CSV files in a 'data' directory.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    os.makedirs(data_dir, exist_ok=True)  # Ensure data directory exists
    file_path = os.path.join(data_dir, f"{dataset_id}.csv")
    if not os.path.exists(file_path):
        raise ValueError(f"Dataset '{dataset_id}' not found at {file_path}")
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load dataset '{dataset_id}': {str(e)}")


# Common schema for dataset_id parameter
DATASET_SCHEMA = {
    "type": "object",
    "properties": {
        "dataset_id": {
            "type": "string",
            "description": "The unique identifier of the dataset to analyze"
        }
    },
    "required": ["dataset_id"]
}
