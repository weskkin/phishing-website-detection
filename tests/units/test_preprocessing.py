import pytest
import pandas as pd
import numpy as np
from src.preprocessing import load_raw_data, handle_missing_values , drop_unnecessary_columns

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