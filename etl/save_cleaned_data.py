from pathlib import Path
import numpy as np
import pandas as pd

# Reset index and save cleaned data

def save_data(df: pd.DataFrame, filepath: str):
    df = df.reset_index(drop = True)
    ext = Path(filepath).suffix.lower()
    if ext == ".csv":
        df.to_csv(filepath, index=False)
    elif ext in (".xlsx", ".xls"):
        df.to_excel(filepath, index=False)
    else:
        df.to_csv(filepath, index=False)
    

