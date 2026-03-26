import argparse
import os
import re
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import logging
from etl import load_data, save_data, generate_summary
from cleaners import (clean_column_names, handle_missing_values, infer_and_convert_types,
                      clean_numeric_cols, remove_empty, standardise_categories, 
                      clean_currency_columns, clean_strings, clean_date_columns
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
) 
logger = logging.getLogger(__name__) 

# Configuration: Define schema here
CURRENCY_COLS = ['price'] # 'discount_amount', 'shipping_fee' etc. the list of currency cols to be cleaned
DATE_COLS = ['added_date'] #list all date cols

# MAIN PIPELINE

def clean_pipeline(input_path: str, output_path: str):
    logger.info(f"\n{'='*50}")
    logger.info(f"  DATA CLEANER — {input_path}")
    logger.info(f"{'='*50}\n")
    
    logger.info("[1/10] Loading data...")
    df = load_data(input_path)
    logger.info(f"Shape of original data: {df.shape}")

    logger.info("[2/10] Cleaning column names...")
    df = clean_column_names(df)
    logger.info(f"  ✔ Column names standardised")

    logger.info("[3/10] Removing empty rows/columns...")
    df = remove_empty(df)
    logger.info(f"  ✔ Removed near-empty columns and rows, and duplicated rows")

    logger.info("[4/10] Cleaning string values...")
    df = clean_strings(df)

    logger.info("[5/10] Inferring & converting data types...")
    df = infer_and_convert_types(df)
    logger.info(f"  ✔ Data types inferred where possible")

    logger.info('[6/10] Cleaning date columns...')
    df = clean_date_columns(df, DATE_COLS)

    logger.info("[7/10] Cleaning currency columns...")
    df = clean_currency_columns(df, CURRENCY_COLS)

    logger.info("[8/10] Cleaning numeric columns & flagging outliers...")
    df = clean_numeric_cols(df)
    logger.info(f"  ✔ Numeric columns cleaned & outliers flagged")

    logger.info("[9/10] Handling missing values...")
    df = handle_missing_values(df)
    logger.info(f"  ✔ Missing values handled (median / ffill / 'Unknown')")

    logger.info("[10/10] Standardising categories & finalising...")
    df = standardise_categories(df)
    logger.info(f"  ✔ Low-cardinality string columns standardised to Categorical")

    logger.info("Cleaning finished. Getting summary of resulting df")
    generate_summary(df)

    logger.info("Saving...")
    save_data(df, output_path)

    logger.info("✅  All done.\n")
    return df


# CLI ENTRY POINT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal daily data cleaner")
    parser.add_argument("--input",  "-i", required=True,  help="Path to raw input file (CSV or Excel)")
    parser.add_argument("--output", "-o", required=False, help="Path to save cleaned file (defaults to <input>_cleaned.csv)")
    args = parser.parse_args()

    input_path = args.input
    if args.output:
        output_path = args.output
    else:
        stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{stem}_cleaned.csv")

    clean_pipeline(input_path, output_path)

# run it: python base_cleaning.py --input data/raw_data.csv --output data/clean_data.csv
# or python data_cleaner.py --input raw_data.csv # auto-names output