import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_date_columns(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    """
    Standardises date columns to YYYY-MM-DD.
    - Handles multiple formats automatically.
    - Coerces invalid dates (e.g., month 13) to NaT (Not a Time).
    """
    if isinstance(date_cols, str):
        date_cols = [date_cols]

    valid_cols = [c for c in date_cols if c in df.columns]

    for col in valid_cols:
        # pd.to_datetime with dayfirst=False is safer for US/General formats
        # errors='coerce' ensures the script doesn't crash on "2023-00-01"
        df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=False)
        
        # Log how many dates failed to parse
        null_count = df[col].isna().sum()
        if null_count > 0:
            logger.warning(f"  ⚠ '{col}': {null_count} rows could not be parsed as dates.")

    logger.info(f"  ✔ Date columns standardised: {valid_cols}")
    return df