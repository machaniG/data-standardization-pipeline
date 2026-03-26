import numpy as np
import pandas as pd

# clean column names

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise column names: strip, lowercase, replace spaces/specials with underscore."""
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[\s\-\.]+", "_", regex=True)
        .str.replace(r"[^\w]", "", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )
    # De-duplicate column names by appending a suffix
    seen = {}
    new_cols = []
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    df.columns = new_cols
    return df
