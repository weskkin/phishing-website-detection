import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from collections import Counter
from pathlib import Path


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
    # Ensure URL column and Domain column are string type and handle missing values
    df['URL'] = df['URL'].fillna('').astype(str)
    df['Domain'] = df['Domain'].fillna('').astype(str)

    df['url_entropy'] = df['URL'].apply(calculate_entropy)
    df['num_params'] = (
        df['URL'].str.split(r'\?').str[1]
          .str.count('&')
          .fillna(0)
        + df['URL'].str.contains(r'\?').astype(int)
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

def preprocess_pipeline(input_path: str, output_dir: str = "data/processed", smote_kwargs=None) -> tuple:
    """ Complete preprocessing workflow """
    # Load dada
    df = load_raw_data(input_path)

    # Clean data
    df = handle_missing_values(df)
    
    # Feature engineering
    df = engineer_features(df)

    # Drop non useful columns
    df = drop_unnecessary_columns(df)
    
    # Encode categorical features
    # The only categorical feature we have is TLD, change later if there are others
    # Or maybe later make a function that detects all categorical features and encodes them
    le = LabelEncoder()
    df['tld_encoded'] = le.fit_transform(df['TLD'])
    df = df.drop(columns=['TLD'])

    # Split features and target
    X = df.drop(columns=['label'])
    y = df['label']

    # Balance classes with safety checks
    class_counts = Counter(y)
    min_class = min(class_counts, key=class_counts.get)
    min_count = class_counts[min_class]
    
    # Auto-adjust k_neighbors for small test datasets
    smote_kwargs = smote_kwargs or {}
    if min_count == 2:
        smote_kwargs['k_neighbors'] = 1
    elif min_count < 2:
        raise ValueError(f"Class {min_class} has only {min_count} samples - need at least 2")
    
    smote = SMOTE(**smote_kwargs)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Save full processed data
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    pd.concat([X, y], axis=1).to_csv(f"{output_dir}/processed_data.csv", index=False)
    # Save features and target separately
    X.to_csv(f"{output_dir}/features.csv", index=False)
    y.to_csv(f"{output_dir}/target.csv", index=False)
    # Save label encoder
    joblib.dump(le, f"{output_dir}/label_encoder.pkl")

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test