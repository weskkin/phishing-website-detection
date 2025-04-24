# Phishing Website Detection 🛡️

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Description

A machine learning tool to detect phishing websites using static dataset features or live URL analysis.

## Features

- Two versions:
  - Version 1: Static analysis with preprocessed features
  - Version 2: Live SSL checks and domain age lookup
- Multiple models: Decision Tree, Logistic Regression, SVM
- Interactive GUI for easy use

## Installation

- Step 1: Clone the repository
  ```bash
  git clone https://github.com/weskkin/phishing-website-detection.git
  ```
- Step 2: Create and activate a virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate.bat  # Windows
  ```
- Step 3: Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
- Step 4: Download the PhiUSIIL dataset and place it in `data/`
  ```bash
  # Ensure the file is named phishing_full.csv
  mv /path/to/phishing_full.csv data/
  ```

## Usage

- **Version 1** (static analysis):
  ```bash
  # Preprocess dataset
  python versions/v1/preprocess.py --input data/phishing_full.csv --output data/processed.csv
  # Train model
  python versions/v1/train.py --data data/processed.csv --model models/v1/model.pkl
  # Launch GUI
  python versions/v1/gui.py
  ```

- **Version 2** (live URL analysis):
  ```bash
  python versions/v2/live_analysis.py
  ```

## Project Structure

```
phishing-website-detection/
├── versions/
│  ├── v1/
│  │  ├── preprocess.py
│  │  ├── train.py
│  │  └── gui.py
│  └── v2/
│     └── live_analysis.py
├── data/
│  └── phishing_full.csv
├── models/
│  ├── v1/
│  │  └── model.pkl
│  └── v2/
├── requirements.txt
└── LICENSE
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

- Fork the repository
- Create your feature branch
  ```bash
  git checkout -b feature/YourFeature
  ```
- Commit your changes
  ```bash
  git commit -m "Add your feature"
  ```
- Push to the branch
  ```bash
  git push origin feature/YourFeature
  ```
- Open a pull request
