import pytest
import pandas as pd
from src.preprocessing import load_raw_data


def test_load():
    # Direct path assuming tests are run from project root

    # Test with sample data
    data = load_raw_data("tests/test_data/full_sample.csv")

    # Basic checks
    assert isinstance(data, pd.DataFrame), "Should return Dataframe"
    assert not data.empty, "Data should not be empty"
    print("Load test passed !")

if __name__ == "__main__":
    test_load()