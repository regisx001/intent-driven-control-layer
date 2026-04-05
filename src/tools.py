from pathlib import Path
from typing import List, Optional

import pandas as pd


DATASETS_DIR = Path(__file__).resolve().parent.parent / "datasets"
MAX_ROWS = 200


def _normalize_dataset_name(dataset: str) -> str:
    dataset = dataset.strip()
    if not dataset.lower().endswith(".csv"):
        dataset = f"{dataset}.csv"
    return dataset


def _dataset_path(dataset: str) -> Path:
    return DATASETS_DIR / _normalize_dataset_name(dataset)


def _load_dataset(dataset: str) -> pd.DataFrame:
    path = _dataset_path(dataset)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset '{path.name}' was not found in {DATASETS_DIR}")
    return pd.read_csv(path)


def _safe_row_count(n_rows: int, default: int = 5) -> int:
    if not isinstance(n_rows, int):
        return default
    if n_rows <= 0:
        return default
    return min(n_rows, MAX_ROWS)


def list_datasets() -> str:
    """List all CSV datasets available in the datasets folder."""
    files = sorted(path.name for path in DATASETS_DIR.glob("*.csv"))
    if not files:
        return "No CSV datasets were found in the datasets directory."
    return pd.DataFrame({"dataset": files}).to_markdown(index=False)


def get_dataset_overview(dataset: str) -> str:
    """
    Return high-level dataset metadata and schema information.

    Args:
        dataset: dataset name with or without .csv extension

    Returns:
        A markdown-formatted overview table and schema table.
    """
    try:
        df = _load_dataset(dataset)
    except Exception as error:
        return f"Error reading file: {error}"

    overview = pd.DataFrame(
        [
            {
                "rows": int(df.shape[0]),
                "columns": int(df.shape[1]),
                "missing_values": int(df.isna().sum().sum()),
                "duplicate_rows": int(df.duplicated().sum()),
                "memory_mb": round(float(df.memory_usage(deep=True).sum() / 1024**2), 3),
            }
        ]
    )

    schema = (
        df.dtypes.astype(str)
        .reset_index()
        .rename(columns={"index": "column", 0: "dtype"})
    )

    return (
        "Dataset Overview\n"
        f"{overview.to_markdown(index=False)}\n\n"
        "Schema\n"
        f"{schema.to_markdown(index=False)}"
    )


def get_first_rows(dataset: str, n_rows: int = 5) -> str:
    """Get the first n rows for a given dataset."""
    n_rows = _safe_row_count(n_rows)
    try:
        df = _load_dataset(dataset)
        return df.head(n_rows).to_markdown()
    except Exception as error:
        return f"Error reading file: {error}"


def get_last_rows(dataset: str, n_rows: int = 5) -> str:
    """
    Get the last n rows for a given dataset.

    Args:
        dataset: dataset name with or without .csv extension
        n_rows: number of rows to return

    Returns:
        A string containing the last n rows in markdown format.
    """
    n_rows = _safe_row_count(n_rows)
    try:
        df = _load_dataset(dataset)
        return df.tail(n_rows).to_markdown()
    except Exception as error:
        return f"Error reading file: {error}"


def get_missing_values(dataset: str, top_n: int = 20) -> str:
    """
    Report columns with missing values.

    Args:
        dataset: dataset name with or without .csv extension
        top_n: max number of columns to display

    Returns:
        A markdown table sorted by missing count.
    """
    try:
        df = _load_dataset(dataset)
    except Exception as error:
        return f"Error reading file: {error}"

    missing_counts = df.isna().sum()
    missing_counts = missing_counts[missing_counts > 0].sort_values(
        ascending=False)

    if missing_counts.empty:
        return "No missing values were found in this dataset."

    top_n = _safe_row_count(top_n, default=20)
    report = pd.DataFrame(
        {
            "column": missing_counts.index,
            "missing_count": missing_counts.values,
            "missing_pct": (missing_counts.values / len(df) * 100).round(2),
        }
    ).head(top_n)
    return report.to_markdown(index=False)


def get_numeric_summary(dataset: str, columns: Optional[List[str]] = None) -> str:
    """
    Produce descriptive statistics for numeric columns.

    Args:
        dataset: dataset name with or without .csv extension
        columns: optional list of numeric columns to include

    Returns:
        Markdown table with descriptive statistics.
    """
    try:
        df = _load_dataset(dataset)
    except Exception as error:
        return f"Error reading file: {error}"

    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return "This dataset has no numeric columns for summary statistics."

    if columns:
        missing_cols = [
            col for col in columns if col not in numeric_df.columns]
        if missing_cols:
            return f"These columns are missing or non-numeric: {missing_cols}"
        numeric_df = numeric_df[columns]

    summary = numeric_df.describe().transpose()
    summary["missing_count"] = numeric_df.isna().sum()
    summary["missing_pct"] = (
        summary["missing_count"] / len(df) * 100).round(2)
    return summary.round(4).to_markdown()


def get_correlation_matrix(
    dataset: str,
    columns: Optional[List[str]] = None,
    method: str = "pearson",
) -> str:
    """
    Compute a correlation matrix on numeric columns.

    Args:
        dataset: dataset name with or without .csv extension
        columns: optional list of numeric columns to include
        method: one of pearson, spearman, kendall

    Returns:
        Correlation matrix in markdown format.
    """
    valid_methods = {"pearson", "spearman", "kendall"}
    if method not in valid_methods:
        return f"Invalid method '{method}'. Use one of: {sorted(valid_methods)}"

    try:
        df = _load_dataset(dataset)
    except Exception as error:
        return f"Error reading file: {error}"

    numeric_df = df.select_dtypes(include="number")
    if columns:
        missing_cols = [
            col for col in columns if col not in numeric_df.columns]
        if missing_cols:
            return f"These columns are missing or non-numeric: {missing_cols}"
        numeric_df = numeric_df[columns]

    if numeric_df.shape[1] < 2:
        return "Correlation requires at least 2 numeric columns."

    corr = numeric_df.corr(method=method).round(4)
    return corr.to_markdown()


def get_groupby_aggregation(
    dataset: str,
    by: str,
    target: str,
    agg: str = "mean",
    top_n: int = 10,
) -> str:
    """
    Aggregate a target column grouped by another column.

    Args:
        dataset: dataset name with or without .csv extension
        by: grouping column
        target: target column to aggregate
        agg: aggregation function (mean, sum, min, max, median, count, nunique, std, var)
        top_n: maximum rows to return

    Returns:
        Markdown table with grouped aggregation.
    """
    valid_aggregations = {
        "mean",
        "sum",
        "min",
        "max",
        "median",
        "count",
        "nunique",
        "std",
        "var",
    }

    if agg not in valid_aggregations:
        return f"Invalid aggregation '{agg}'. Use one of: {sorted(valid_aggregations)}"

    try:
        df = _load_dataset(dataset)
    except Exception as error:
        return f"Error reading file: {error}"

    if by not in df.columns:
        return f"Column '{by}' does not exist in the dataset."
    if target not in df.columns:
        return f"Column '{target}' does not exist in the dataset."

    if agg in {"mean", "sum", "min", "max", "median", "std", "var"} and not pd.api.types.is_numeric_dtype(df[target]):
        return f"Aggregation '{agg}' requires a numeric target column."

    result = (
        df.groupby(by, dropna=False)[target]
        .agg(agg)
        .reset_index()
        .rename(columns={target: f"{target}_{agg}"})
        .sort_values(by=f"{target}_{agg}", ascending=False)
    )

    top_n = _safe_row_count(top_n, default=10)
    return result.head(top_n).to_markdown(index=False)


def get_value_counts(dataset: str, column: str, top_n: int = 10) -> str:
    """
    Get frequency counts for a categorical or discrete column.

    Args:
        dataset: dataset name with or without .csv extension
        column: column to count values for
        top_n: number of values to return

    Returns:
        Markdown table with value counts.
    """
    try:
        df = _load_dataset(dataset)
    except Exception as error:
        return f"Error reading file: {error}"

    if column not in df.columns:
        return f"Column '{column}' does not exist in the dataset."

    top_n = _safe_row_count(top_n, default=10)

    counts = (
        df[column]
        .fillna("<NA>")
        .value_counts(dropna=False)
        .head(top_n)
        .reset_index()
    )
    counts.columns = [column, "count"]
    counts["pct"] = (counts["count"] / len(df) * 100).round(2)
    return counts.to_markdown(index=False)


available_tools = [
    list_datasets,
    get_dataset_overview,
    get_first_rows,
    get_last_rows,
    get_missing_values,
    get_numeric_summary,
    get_correlation_matrix,
    get_groupby_aggregation,
    get_value_counts,
]
