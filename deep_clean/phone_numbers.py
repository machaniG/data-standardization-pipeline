import pandas as pd
import re

def format_phone_numbers(df):
    """Strips formatting to leave only digits."""
    if 'phone' in df.columns:
        # Remove all non-digit characters (brackets, spaces, dashes)
        df['phone'] = df['phone'].astype(str).str.replace(r'\D', '', regex=True)
        
        # Handle cases where the field was empty
        df['phone'] = df['phone'].replace('', 'No Phone Provided')
    
    return df