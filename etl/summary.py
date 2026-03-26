import numpy as np
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
) 
logger = logging.getLogger(__name__) 


def generate_summary(df: pd.DataFrame):
    df = df.reset_index(drop=True)
    logger.info("\n──── CLEANED DATA SUMMARY ────")
    logger.info(f"  Shape      : {df.shape[0]} rows × {df.shape[1]} columns")
    logger.info(f"  Dtypes     :\n{df.dtypes.value_counts().to_string()}")
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]
    if null_counts.empty:
        logger.info("  Nulls      : None remaining")
    else:
        logger.info(f"  Nulls      :\n{null_counts.to_string()}")
    logger.info("──────────────────────────────\n")

