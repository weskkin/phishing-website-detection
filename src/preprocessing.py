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

# def handle_missing_values(df: pd.DataFrame) -> pd.Dataframe:
#     # Check for missing labels
#     missing_labels = df['label'].isnull().sum()
#     print(f"Found {missing_labels} rows with missing labels")

#     # Remove rows with missing 

# def calculate_entropy(url: str) -> float:
#     """Calculate Shannon entropy of a URL string"""
#     # Convert URL to list of characters
#     chars = list(url)
    
#     # Count frequency of each unique character
#     unique_chars, counts = np.unique(chars, return_counts=True)
    
#     # Calculate probability of each character
#     probabilities = counts / len(url)
    
#     # Compute entropy using Shannon formula
#     entropy = -np.sum(probabilities * np.log2(probabilities))
    
#     return entropy

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

# # divide drop columns and handle missing values
# def clean_data(df: pd.DataFrame) -> pd.DataFrame:
#     """ 
#     1. Drop unnecessary columns
#     2. Handle missing values
#     """

#     # Remove unnecessary columns
#     df.drop(columns=["FILENAME","Title","Domain","URL"])

#     # Handle missing labels
#     if df['label'].isnull().sum() > 0:
#         df = df.dropna(subset=['label'])

#     return df