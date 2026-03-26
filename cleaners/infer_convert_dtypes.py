import numpy as np
import pandas as pd

# Data type inference and conversion 

def infer_and_convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Try to convert object columns to numeric or datetime where sensible.
    Columns that fail conversion stay as-is.
    """
    for col in df.select_dtypes(include="object").columns:
        # Attempt numeric
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.notna().sum() / max(df[col].notna().sum(), 1) > 0.8:
            df[col] = converted
            continue

        # Attempt datetime
        try:
            converted_dt = pd.to_datetime(df[col], errors="coerce", infer_datetime_format=True)
            if converted_dt.notna().sum() / max(df[col].notna().sum(), 1) > 0.8:
                df[col] = converted_dt
        except Exception:
            pass

    return df
