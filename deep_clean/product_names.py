import pandas as pd
import numpy as np
import logging
from rapidfuzz import process

logger = logging.getLogger(__name__)

def standardize_product_names(df: pd.DataFrame, col: str, reference_list: list) -> pd.DataFrame:
    """
    Cleans strings and uses fuzzy matching to map messy names to a 
    standardized reference list of products.
    e.g., fuzzy matching will change Vit4Min D3 to Vitamin D3 Gold
    """
    if col not in df.columns:
        return df

    # 1. Preliminary "Hard" Cleaning (Regex)
    # This makes the fuzzy matcher's job much easier
    df[col] = (
        df[col].astype(str)
        .str.replace("_", " ", regex=False)        # Remove underscores
        .str.replace(r"[!@#$%^&*]", "", regex=True) # Remove noise chars
        .str.replace("3", "e").str.replace("4", "a") # Reverse common leet-speak
        .str.strip().str.title()
    )

    # 2. Fuzzy Mapping
    # We find the closest match in the reference_list for every unique messy name
    unique_messy_names = df[col].unique()
    
    mapping_dict = {}
    for name in unique_messy_names:
        if pd.isna(name) or name.lower() == 'nan':
            continue
        
        # Find the best match from your known "Good" products
        # score_cutoff=70 ensures we don't match completely random strings
        match, score, index = process.extractOne(name, reference_list)
        
        if score >= 70:
            mapping_dict[name] = match
        else:
            mapping_dict[name] = name # Keep original if no confident match

    df[col] = df[col].map(mapping_dict)
    
    logger.info(f"  ✔ Standardized {len(mapping_dict)} unique product variants in '{col}'")
    return df

