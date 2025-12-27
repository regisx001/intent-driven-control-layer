from typing import Callable, Dict, Any
from .tools.quality import detect_missing_values
from .tools.schema import analyze_schema
from .tools.stats import compute_basic_stats


class Tool:
    def __init__(self, name, description, schema, fn: Callable):
        self.name = name
        self.description = description
        self.schema = schema
        self.fn = fn


# Hardcoded tools
TOOLS = {
    "detect_missing_values": {
        "description": "Analyze a dataset to detect missing values in each column, returning the proportion of missing values per column.",
        "schema": {
            "type": "object",
            "properties": {
                "dataset_id": {
                    "type": "string",
                    "description": "The unique identifier of the dataset to analyze"
                }
            },
            "required": ["dataset_id"]
        },
        "function": detect_missing_values
    },
    "analyze_schema": {
        "description": "Analyze the schema of a dataset, providing column names, data types, and missing value counts.",
        "schema": {
            "type": "object",
            "properties": {
                "dataset_id": {
                    "type": "string",
                    "description": "The unique identifier of the dataset to analyze"
                }
            },
            "required": ["dataset_id"]
        },
        "function": analyze_schema
    },
    "compute_basic_stats": {
        "description": "Compute basic statistics for a dataset, including number of rows, columns, and descriptive statistics for numeric columns.",
        "schema": {
            "type": "object",
            "properties": {
                "dataset_id": {
                    "type": "string",
                    "description": "The unique identifier of the dataset to analyze"
                }
            },
            "required": ["dataset_id"]
        },
        "function": compute_basic_stats
    }
}


def get_tool(name: str) -> Tool:
    return TOOLS.get(name)


def list_tools() -> Dict[str, Tool]:
    return TOOLS
