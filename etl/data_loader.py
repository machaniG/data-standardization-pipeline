from pathlib import Path
import numpy as np
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
) 
logger = logging.getLogger(__name__) 

# Load data
def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV or Excel file into a DataFrame."""
    ext = Path(filepath).suffix.lower()
    if ext == ".csv":
        # Try multiple encodings & separators
        for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
            try:
                df = pd.read_csv(filepath, encoding=enc, sep=None, engine="python",
                                 on_bad_lines="warn")
                logger.info(f"  Loaded CSV with encoding '{enc}': {df.shape[0]} rows × {df.shape[1]} cols")
                return df
            except Exception:
                continue
        raise ValueError(f"Could not read CSV: {filepath}")
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(filepath)
        logger.info(f"  Loaded Excel: {df.shape[0]} rows × {df.shape[1]} cols")
        return df
    else:
        raise ValueError(f"Unsupported file type: {ext}")