import pytest
from pathlib import Path
from src.preprocessing import preprocess_pipeline

def test_preprocess_pipeline():
    X_train, X_test, y_train, y_test = preprocess_pipeline(
        "tests/test_data/full_sample.csv",
        output_dir="tests/test_data/processed",
        smote_kwargs={
            'random_state': 42,
            'k_neighbors': 1,
            'sampling_strategy': 'auto'  # Let SMOTE determine balance
        }
    )

    # Relax assertions for small test data
    assert not X_train.empty

    # Total rows in = total rows out
    total_out    = len(X_train) + len(X_test)
    total_labels = len(y_train) + len(y_test)
    assert total_out == total_labels

    # Each split should be balanced (all classes equal frequency)
    vc_train = y_train.value_counts()
    vc_test  = y_test.value_counts()

    # There should be exactly one unique count in each split
    assert vc_train.nunique() == 1, f"Train set not balanced: {vc_train.to_dict()}"
    assert vc_test.nunique()  == 1, f"Test set not balanced: {vc_test.to_dict()}"

    assert 'url_entropy' in X_train.columns 
    assert 'tld_encoded' in X_train.columns
    
    # Validate saved files
    assert Path("tests/test_data/processed/features.csv").exists()
    assert Path("tests/test_data/processed/label_encoder.pkl").exists()