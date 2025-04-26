import pytest
import pandas as pd
import numpy as np
from src.preprocessing import load_raw_data, handle_missing_values , drop_unnecessary_columns , calculate_entropy , engineer_features

# Test 1
def test_load():
    # Direct path assuming tests are run from project root

    # Test with sample data
    data = load_raw_data("tests/test_data/full_sample.csv")

    # Basic checks
    assert isinstance(data, pd.DataFrame), "Should return Dataframe"
    assert not data.empty, "Data should not be empty"
    print("Load test passed !")


# Test 2
def test_missing_values_handling():
    # Create test data with missing values
    test_data = pd.DataFrame({
        'label': [0, np.nan, 1, None],
        'feature1': [1,2,3,4],
        'feature2': [5,6,7,8]
    })

    cleaned_data = handle_missing_values(test_data)

    # Should remove 2 rows with missing values
    assert len(cleaned_data) == 2
    assert cleaned_data['label'].isna().sum() == 0

def test_no_missing_values():
    # Create test data with no missing values
    test_data = pd.DataFrame({
        'label': [0,1,0],
        'feature1': [1,2,3]
    })

    cleaned_data = handle_missing_values(test_data)
    assert len(cleaned_data) == 3

# Test 3
def test_drop_unnecessary_columns():
    # Test normal case
    test_df = pd.DataFrame({
        'FILENAME': ['a.html'],
        'URL': ['http://test.com'],
        'Domain': ['test.com'],
        'Title': ['Test Site'],
        'URLLength': [15],
        'IsHTTPS': [1]
    })
    
    cleaned = drop_unnecessary_columns(test_df)
    
    # Verify unwanted columns removed
    assert 'FILENAME' not in cleaned.columns
    assert 'URL' not in cleaned.columns
    assert 'Domain' not in cleaned.columns
    assert 'Title' not in cleaned.columns
    
    # Verify important columns remain
    assert 'URLLength' in cleaned.columns
    assert 'IsHTTPS' in cleaned.columns

def test_drop_columns_missing_some():
    # Test with partial columns
    test_df = pd.DataFrame({
        'URL': ['http://test.com'],
        'URLLength': [15]
    })
    
    cleaned = drop_unnecessary_columns(test_df)
    assert 'URL' not in cleaned.columns
    assert 'URLLength' in cleaned.columns

def test_drop_no_columns():
    # Test with none of the columns present
    test_df = pd.DataFrame({'URLLength': [15], 'IsHTTPS': [1]})
    cleaned = drop_unnecessary_columns(test_df)
    assert len(cleaned.columns) == 2

# Test 4
def test_calculate_entropy_basic():
    # Test with repeated characters (low entropy)
    assert calculate_entropy("aaaaa") == pytest.approx(0.0, abs=1e-3)  # All same characters
    
    # Test with varied characters (high entropy)
    assert calculate_entropy("aBcDeF123!@#") == pytest.approx(3.58496, abs=1e-3)

def test_calculate_entropy_edge_cases():
    # Empty string
    assert calculate_entropy("") == 0.0
    
    # Single character
    assert calculate_entropy("x") == 0.0
    
    # URL with special characters
    assert calculate_entropy("http://example.com/?q=test&id=123") == pytest.approx(4.332, abs=1e-3)

def test_entropy_calculation_consistency():
    # Verify same URL produces same entropy
    url1 = "https://secure-bank.com/login"
    url2 = "https://secure-bank.com/login"
    assert calculate_entropy(url1) == calculate_entropy(url2)
    
    # Different URLs different entropy
    phish_url = "hXXp5://s3cur3-b4nk.com/l0g1n_abc123!"
    assert calculate_entropy(phish_url) > calculate_entropy(url1)

# Test 5
def test_engineer_features():
    test_data = pd.DataFrame({
        'URL': [
            'https://paypal.com/login?user=1&session=abc',  # 2 params
            'http://sub.sub2.paypa1-security.xyz:8080/%25%26',  # No params
            'http://simple.com?search=test'  # 1 param
        ],
        'Domain': ['paypal.com', 'sub.sub2.paypa1-security.xyz', 'simple.com'],
        'TLD': ['com', 'xyz', 'com'],
        'DomainTitleMatchScore': [0.9, 0.3, 0.6],
        'IsHTTPS': [1, 0, 0],
        'ObfuscationRatio': [0.1, 0.8, 0.2],
        'NoOfExternalRef': [2, 5, 1]
    })
    
    processed = engineer_features(test_data)
    
    # Test Parameter Count
    assert processed['num_params'][0] == 2, "2 parameters: user & session"
    assert processed['num_params'][1] == 0, "No query parameters"
    assert processed['num_params'][2] == 1, "Single parameter: search"
    
    # Test Subdomain Levels (Count of dots)
    assert processed['subdomain_level'][0] == 1, "paypal.com → 1 dot"
    assert processed['subdomain_level'][1] == 3, "sub.sub2.paypa1-security.xyz → 3 dots"
    assert processed['subdomain_level'][2] == 1, "simple-domain.com → 1 dot"
    
    # Test TLD Suspicion
    assert processed['tld_suspicious'][1] == 1, ".xyz should be flagged"
    
    # Test Brand Mismatch
    assert processed['brand_mismatch'][1] == 1, "Low title match score"
    
    # Test Risk Score
    assert processed['risk_score'][1] > processed['risk_score'][0], "Phishing sample higher risk"
    assert processed['risk_score'][2] < processed['risk_score'][1], "Legitimate lower risk"