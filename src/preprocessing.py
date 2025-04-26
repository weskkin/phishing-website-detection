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

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """ Derive new features """

    # URL Structure Features
    df['url_entropy'] = df['URL'].apply(calculate_entropy)
    df['num_params'] = (
        df['URL'].str.split('?').str[1].str.count('&').fillna(0) + 
        df['URL'].str.contains(r'\?').astype(int)  # Changed '?' to r'\?'
    )  # Count URL parameters
    df['subdomain_level'] = df['Domain'].str.count(r'\.')  # Subdomain depth
    
    # Domain Analysis
    df['tld_suspicious'] = df['TLD'].isin(['xyz', 'top', 'cc', 'tk']).astype(int)
    df['hyphen_count'] = df['Domain'].str.count('-')
    df['num_encoded_chars'] = df['URL'].str.count(r'%[0-9a-fA-F]{2}')  # Hex encoding
    
    # Content Features
    df['login_keyword'] = df['URL'].str.contains(r'login|signin|auth', case=False).astype(int)
    df['brand_mismatch'] = (
        df['DomainTitleMatchScore'] < 0.5
    ).astype(int)  # Domain vs page title
    
    # Security Features
    df['mixed_content'] = (
        df['IsHTTPS'] & 
        df['NoOfExternalRef'].gt(0)
    ).astype(int)  # HTTPS but external HTTP links
    
    # Compound Metrics
    df['risk_score'] = (
        0.3 * df['ObfuscationRatio'] +
        0.2 * df['url_entropy'] +
        0.2 * df['tld_suspicious'] +
        0.3 * df['brand_mismatch']
    )
    
    return df

    # def preprocess_pipeline(input_path: str, output_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    # """Updated workflow using your actual columns"""
    # # Load data
    # df = load_data(input_path)
    
    # # Clean data - remove rows with missing labels
    # df = clean_data(df)
    
    # # Feature engineering (using real columns)
    # df = engineer_features(df)
    
    # # Handle missing values
    # df = handle_missing_values(df)
    
    # # Encode categorical features
    # categorical_cols = ['TLD']  # From your column list
    # for col in categorical_cols:
    #     le = LabelEncoder()
    #     df[col] = le.fit_transform(df[col])
    
    # # Split features and target
    # X = df.drop('label', axis=1)
    # y = df['label']
    
    # # Balance classes
    # X_resampled, y_resampled = SMOTE().fit_resample(X, y)
    
    # # Save processed data
    # processed_df = pd.concat([X_resampled, y_resampled], axis=1)
    # processed_df.to_csv(output_path, index=False)
    
    # return X_resampled, y_resampled