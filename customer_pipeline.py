import pandas as pd
import re
from rapidfuzz import process
from pathlib import Path
import logging
from etl import load_data, save_data, generate_quality_report
from deep_clean import (clean_emails, standardize_headers, clean_customer_names, 
                      clean_addresses, format_phone_numbers, ensure_full_name)
import argparse

logger = logging.getLogger(__name__) 


def run_customer_integration(google_path: str, xero_path: str, output_path: str):
    # 1. Load and align headers (column names)
    logger.info("Step 1: Loading customer files and aligning column names...")
    google_df = standardize_headers(load_data(google_path))
    xero_df = standardize_headers(load_data(xero_path))

    # 2. Standardize names cols to one full name col
    logger.info("Step 2: Aligning customer names...")
    xero_df = ensure_full_name(xero_df)
    google_df = ensure_full_name(google_df)
    logger.info("Customers now have full names...")

    # 3. Stack them together (Concatenate) to combine customer list
    customer_df = pd.concat([google_df, xero_df], ignore_index=True)
    # Fill NaN in Company with an Not available
    customer_df['company'] = customer_df['company'].fillna('Individual').str.strip()
    logger.info("Customer lists combined")

    # deep Clean
    customer_df = clean_customer_names(customer_df)
    customer_df = clean_emails(customer_df) # also removes duplicates using email as unique identifier
    customer_df = format_phone_numbers(customer_df)
    customer_df = clean_addresses(customer_df)

    #save
    logger.info("Cleaning finished. Getting summary report..")
    generate_quality_report(customer_df)
    
    logger.info("Saving clean customer data...")
    save_data(customer_df, output_path)

    return customer_df

# CLI ENTRY POINT

if __name__ == "__main__":
    # 1. Setup the Argument Parser
    parser = argparse.ArgumentParser(
        description="Customer Data Integration & Deep Cleaning Pipeline",
        epilog="Example: python customer_pipeline.py google_raw.csv xero_raw.csv clean_customers.csv"
    )
    
    # 2. Add Positional Arguments (Required)
    parser.add_argument("google_input", help="Path to the raw Google Contacts CSV")
    parser.add_argument("xero_input", help="Path to the raw Xero Customers CSV")
    parser.add_argument("output", help="Path to save the consolidated Master Customer List")

    # 3. Add Optional Arguments
    parser.add_argument(
        "--log-level", 
        default="INFO", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set the logging threshold (default: INFO)"
    )

    # 4. Parse the arguments
    args = parser.parse_args()

    # 5. Configure Logging based on CLI input
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

    # 6. Execute the Pipeline
    try:
        run_customer_integration(
            google_path=args.google_input,
            xero_path=args.xero_input,
            output_path=args.output
        )
        print("\n✨ Pipeline Execution Successful!")
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")

# python customer_pipeline.py data/google_raw.csv data/xero_raw.csv data/master_customers.csv
# python customer_pipeline.py data/google_contacts.xlsx data/xero_contacts.csv data/clean_customers.csv