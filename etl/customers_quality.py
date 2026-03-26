import pandas as pd
import logging

logger = logging.getLogger(__name__) 

def generate_quality_report(df):
    """
    Prints a summary of the data health after deep cleaning.
    """
    total_records = len(df)
    
    # Calculate Metrics
    invalid_emails = (~df['is_valid_email']).sum()
    missing_phones = (df['phone'] == 'No Phone Provided').sum()
    unknown_names = (df['full_name'] == 'Unknown').sum()
    individual_customers = (df['company'] == 'Individual').sum()
    missing_emails = (df['email'] == 'no_email_provided').sum()
   

    logger.info("-" * 40)
    logger.info("📋 CUSTOMER DATA QUALITY REPORT")
    logger.info("-" * 40)
    logger.info(f"Total Records Processed: {total_records}")
    logger.info(f"✅ Valid Email Rate:    {((total_records - invalid_emails) / total_records):.1%}")
    logger.info(f"📧 Missing Emails:      {missing_emails} rows")
    logger.info(f"📱 Missing Phone Rate:   {(missing_phones / total_records):.1%}")
    logger.info(f"👤 'Unknown' Name Rate:  {(unknown_names / total_records):.1%}")
    logger.info(f"🏢 B2B vs B2C Ratio:     {1 - (individual_customers / total_records):.1%} Business")
    logger.info("-" * 40)
    
    if invalid_emails > 0:
        logger.info(f"⚠️ Action Required: {invalid_emails} emails failed validation.")
    logger.info("-" * 40)