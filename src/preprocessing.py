"""
Data preprocessing pipeline for phishing detection
Handles cleaning, feature engineering, and balancing
"""

import pandas as pd
import numpy as np

def load_raw_data(path: str) -> pd.DataFrame:
    """ Load raw dataset from specefied path """
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at {path}")



def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """ Remove entries with missing class labels """

    # Check for entries with missing labels
    missing_labels = df['label'].isnull().sum()
    print(f"Found {missing_labels} entries with missing labels")

    # Remove entries with missing lables
    cleaned_df = df.dropna(subset=['label']).copy()

    return cleaned_df

def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ Drop columns (features) that are meaningless or redundant """

    new_df = df.drop(columns=["FILENAME","Title","Domain","URL"], errors='ignore')

    return new_df

def calculate_entropy(url: str) -> float:
    """ Calculate Shannon entropy of a URL string """
    # Handle empty string case
    if not url:  
        return 0.0

    # Convert URL to list of characters
    chars = list(url)
    
    # Count frequency of each unique character
    unique_chars, counts = np.unique(chars, return_counts=True)
    
    # Calculate probability of each character
    probabilities = counts / len(url)
    
    # Compute entropy using Shannon formula
    entropy = -np.sum(probabilities * np.log2(probabilities))
    
    return entropy

# def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
#     """ Create new features """

#     # 1. URL entropy (measure of randomness in URL characters) 
#     df['url_entropy'] = df['URL'].apply(calculate_entropy)

#     # Domain name length
#     df['domain_length'] = df['Domain'].apply(len)
#     # TLD legitimacy probability
#     df['tld_trust_score'] = df['TLDLegitimateProb']
#     # URL structure anomaly detection
#     df['url_depth'] = df['URL'].apply(lambda x: x.count('/'))
#     # HTTPS presence
#     df['uses_https'] = df['URL'].str.startswith('https').astype(int)

