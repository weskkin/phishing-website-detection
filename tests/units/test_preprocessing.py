import pytest
import pandas as pd
import numpy as np
from src.preprocessing import load_raw_data, handle_missing_values

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

