"""
Creates sample test data will all original columns
"""

import pandas as pd
from pathlib import Path

TEST_DATA = {
    # Metadata columns (to be dropped later)
    "FILENAME": [
        "safe1.html",
        "phish1.html",
        "phish2.html",
        "safe2.html",
        "safe3.html"
    ],
    "URL": [
        "https://bank.com/login?user=123&session=abc",       # Legit (0)
        "http://phish-paypal.xyz:8080/auth?id=456",          # Phishing (1)
        "http://steal-info.xyz/login.php?session=hijack",    # Phishing (1)
        "https://secure-portal.net/dashboard",               # Legit (0)
        "https://bank2.com/dashboard?acct=789&token=xyz"     # Legit (0) — NEW
    ],
    "Domain": [
        "bank.com",
        "phish-paypal.xyz",
        "steal-info.xyz",
        "secure-portal.net",
        "bank2.com"      # NEW
    ],
    "Title": [
        "Bank Login Portal",
        "Account Verification Required",
        "Update Your Credentials",
        "Secure Dashboard",
        "Bank2 Dashboard"  # NEW
    ],

    # Numerical features (adjusted for 5 samples)
    "URLLength": [38, 45, 52, 28,  40], 
    "DomainLength": [8, 16, 15, 15,  9],    # NEW DomainLength=9 for "bank2.com"
    "IsDomainIP": [0, 0, 0, 0, 0],
    "TLD": ["com", "xyz", "xyz", "net", "com"],

    "URLSimilarityIndex": [0.95, 0.35, 0.28, 0.92, 0.93],
    "CharContinuationRate": [0.07, 0.42, 0.38, 0.06, 0.05],
    "TLDLegitimateProb": [0.98, 0.15, 0.12, 0.97, 0.96],
    "URLCharProb": [0.85, 0.32, 0.28, 0.88, 0.87],
    "TLDLength": [3, 3, 3, 3, 3],
    "NoOfSubDomain": [1, 2, 1, 1, 1],
    "HasObfuscation": [0, 1, 1, 0, 0],
    "NoOfObfuscatedChar": [0, 7, 9, 0, 0],
    "ObfuscationRatio": [0.0, 0.28, 0.35, 0.0, 0.0],
    "NoOfLettersInURL": [22, 25, 28, 20, 24],
    "LetterRatioInURL": [0.68, 0.55, 0.58, 0.71, 0.70],
    "NoOfDegitsInURL": [3, 3, 0, 2, 3],
    "DegitRatioInURL": [0.08, 0.07, 0.0, 0.07, 0.08],
    "NoOfEqualsInURL": [2, 2, 1, 0, 2],
    "NoOfQMarkInURL": [0, 1, 1, 0, 1],
    "NoOfAmpersandInURL": [1, 1, 0, 0, 1],
    "NoOfOtherSpecialCharsInURL": [2, 5, 6, 1, 3],
    "SpacialCharRatioInURL": [0.05, 0.15, 0.18, 0.04, 0.06],
    "IsHTTPS": [1, 0, 0, 1, 1],

    # HTML features
    "LineOfCode": [150, 600, 550, 180, 160],
    "LargestLineLength": [90, 300, 280, 100, 95],
    "HasTitle": [1, 1, 1, 1, 1],
    "DomainTitleMatchScore": [0.92, 0.28, 0.25, 0.90, 0.91],
    "URLTitleMatchScore": [0.90, 0.25, 0.22, 0.88, 0.89],
    "HasFavicon": [1, 0, 0, 1, 1],
    "Robots": [1, 0, 0, 1, 1],
    "IsResponsive": [1, 0, 0, 1, 1],
    "NoOfURLRedirect": [0, 4, 3, 0, 0],
    "NoOfSelfRedirect": [0, 3, 2, 0, 0],
    "HasDescription": [1, 0, 0, 1, 1],
    "NoOfPopup": [0, 3, 2, 0, 0],
    "NoOfiFrame": [0, 2, 1, 0, 0],
    "HasExternalFormSubmit": [0, 1, 1, 0, 0],
    "HasSocialNet": [1, 0, 0, 1, 1],
    "HasSubmitButton": [1, 1, 1, 1, 1],
    "HasHiddenFields": [0, 1, 1, 0, 0],
    "HasPasswordField": [1, 1, 1, 0, 0],

    # Content markers
    "Bank": [1, 0, 0, 0, 1],
    "Pay": [0, 1, 0, 0, 0],
    "Crypto": [0, 0, 0, 1, 0],
    "HasCopyrightInfo": [1, 0, 0, 1, 1],

    # Resource counts
    "NoOfImage": [4, 10, 8, 3, 4],
    "NoOfCSS": [3, 1, 1, 2, 3],
    "NoOfJS": [3, 7, 6, 2, 3],
    "NoOfSelfRef": [6, 1, 1, 4, 5],
    "NoOfEmptyRef": [0, 6, 5, 0, 0],
    "NoOfExternalRef": [2, 9, 7, 1, 2],

    # Target (now 2 legitimate (0) & 3 phishing (1))
    "label": [0, 1, 1, 0, 0]
}


def main():
    output_path = Path("tests/test_data/full_sample.csv")

    df = pd.DataFrame(TEST_DATA)

    df.to_csv(output_path, index=False)
    print(f"Created FULL test data at {output_path}")

if __name__ == "__main__":
    main()