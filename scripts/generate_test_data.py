"""
Creates sample test data will all original columns
"""

import pandas as pd
from pathlib import Path

TEST_DATA = {
    # Metadata columns (to be dropped later)
    "FILENAME": ["safe.html", "phish.html", "mixed.html"],
    "URL": [
        "https://legit-bank.com", 
        "http://paypal-secure-login.xyz", 
        "http://crypto-wallet.update.com"
    ],
    "Domain": ["legit-bank", "paypal-secure-login", "crypto-wallet.update"],
    "Title": ["Bank Portal", "Account Verification", "Crypto Update"],
    
    # Numerical features
    "URLLength": [21, 34, 28],
    "DomainLength": [11, 20, 19],
    "IsDomainIP": [0, 0, 0],
    "TLD": ["com", "xyz", "com"],
    "URLSimilarityIndex": [0.92, 0.45, 0.78],
    "CharContinuationRate": [0.05, 0.32, 0.18],
    "TLDLegitimateProb": [0.97, 0.25, 0.65],
    "URLCharProb": [0.88, 0.42, 0.68],
    "TLDLength": [3, 3, 3],
    "NoOfSubDomain": [1, 3, 2],
    "HasObfuscation": [0, 1, 1],
    "NoOfObfuscatedChar": [0, 5, 3],
    "ObfuscationRatio": [0.0, 0.21, 0.15],
    "NoOfLettersInURL": [15, 18, 20],
    "LetterRatioInURL": [0.71, 0.53, 0.71],
    "NoOfDegitsInURL": [0, 2, 1],
    "DegitRatioInURL": [0.0, 0.06, 0.04],
    "NoOfEqualsInURL": [0, 1, 0],
    "NoOfQMarkInURL": [0, 2, 1],
    "NoOfAmpersandInURL": [0, 3, 1],
    "NoOfOtherSpecialCharsInURL": [0, 4, 2],
    "SpacialCharRatioInURL": [0.0, 0.18, 0.11],
    "IsHTTPS": [1, 0, 0],
    
    # HTML features
    "LineOfCode": [120, 450, 300],
    "LargestLineLength": [80, 250, 180],
    "HasTitle": [1, 1, 1],
    "DomainTitleMatchScore": [0.95, 0.32, 0.65],
    "URLTitleMatchScore": [0.93, 0.28, 0.60],
    "HasFavicon": [1, 0, 0],
    "Robots": [1, 0, 0],
    "IsResponsive": [1, 0, 1],
    "NoOfURLRedirect": [0, 3, 1],
    "NoOfSelfRedirect": [0, 2, 0],
    "HasDescription": [1, 0, 0],
    "NoOfPopup": [0, 2, 1],
    "NoOfiFrame": [0, 1, 0],
    "HasExternalFormSubmit": [0, 1, 0],
    "HasSocialNet": [1, 0, 0],
    "HasSubmitButton": [1, 1, 1],
    "HasHiddenFields": [0, 1, 1],
    "HasPasswordField": [1, 1, 0],
    
    # Content markers
    "Bank": [1, 0, 0],
    "Pay": [0, 1, 0],
    "Crypto": [0, 0, 1],
    "HasCopyrightInfo": [1, 0, 0],
    
    # Resource counts
    "NoOfImage": [3, 8, 5],
    "NoOfCSS": [2, 1, 1],
    "NoOfJS": [2, 5, 3],
    "NoOfSelfRef": [5, 2, 3],
    "NoOfEmptyRef": [0, 4, 2],
    "NoOfExternalRef": [1, 7, 4],
    
    # Target
    "label": [0, 1, 0]
}

def main():
    output_path = Path("tests/test_data/full_sample.csv")

    df = pd.DataFrame(TEST_DATA)

    df.to_csv(output_path, index=False)
    print(f"Created FULL test data at {output_path}")

if __name__ == "__main__":
    main()