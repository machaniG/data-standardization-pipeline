import argparse
import os
import re
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from rapidfuzz import process
import logging
from etl import load_data, save_data, print_summary
from deep_clean import standardize_product_names, standardize_categories, consolidate_skus


# Configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
) 
logger = logging.getLogger(__name__) 

# category list mapping product categories
CATEGORY_MAP = {
    'supps': 'Supplements', 'supplements': 'Supplements', 'nutr.': 'Supplements',
    'drinks': 'Drinks', 'drnks': 'Drinks', 'unknown': 'Uncategorized'
}

# product name reference list
PRODUCT_REFERENCE = [
    "Optimum Whey", "Hydrolyzed Iso", "Vegan Pea Protein", "Creatine Monohydrate",
    "BCAA Flash", "Pre-Workout Explosion", "ZMA Night", "Omega-3 Fish Oil",
    "Multivitamin Daily", "Casein Slow Release", "L-Glutamine Powder",
    "Mass Gainer 3000", "Keto Electrolytes", "Magnesium Citrate", "Vitamin D3 Gold"
]

# cols to groupby for SKU consolidation
GROUP_COLS = ['product_name', 'category_name']

# Execute the steps
def run_master_pipeline(input_path, output_path, tolerance):
    logger.info(f"🚀 Starting Pipeline 2. Input: {input_path}")
    
    # 1. Load Data
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        logger.error(f"File {input_path} not found!")
        return

    # 2. Step-by-Step Cleaning
    logger.info("Step 1: Standardizing Categories...")
    df = standardize_categories(df, 'category_name', CATEGORY_MAP)

    logger.info("Step 2: Fuzzy Matching Product Names...")
    df = standardize_product_names(df, 'product_name', reference_list=PRODUCT_REFERENCE)

    logger.info(f"Step 3: Consolidating SKUs (Tolerance: ${tolerance})...")
    # Using the optimized Short-SKU function we discussed
    df = consolidate_skus(df, group_cols=GROUP_COLS, 
        price_col='price', 
        tolerance_usd=tolerance
    )

    # 3. Final Save
    df.to_csv(output_path, index=False)
    logger.info(f"✅ Pipeline 2 complete. Master inventory saved to: {output_path}")
    logger.info(f"Total Unique SKUs Generated: {df['consolidated_sku_id'].nunique()}")

if __name__ == "__main__":
    # --- CLI ARGUMENT PARSER ---
    parser = argparse.ArgumentParser(description="Master Inventory Data Pipeline (Pipeline 2)")
    
    # Positional arguments
    parser.add_argument("input", help="Path to the output file from Pipeline 1")
    parser.add_argument("output", help="Path to save the master inventory")
    
    # Optional argument with a default value
    parser.add_argument(
        "--tolerance", 
        type=float, 
        default=1.00, 
        help="Price tolerance in USD for SKU grouping (default: 1.00)"
    )

    args = parser.parse_args()

    # Configure Logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    run_master_pipeline(args.input, args.output, args.tolerance)

# python pipeline_2.py data/pipeline1_output.csv data/final_clean_inventory.csv
# python pipeline_2.py in.csv out.csv --tolerance 2.50