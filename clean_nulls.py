import pandas as pd
import json
import os

def clean_nulls_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans a pandas DataFrame by:
    - Dropping completely empty rows
    - Filling missing values for numeric columns with 0
    - Filling missing values for string/object columns with empty string
    """
    df = df.dropna(how='all')  # drop rows that are completely null
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(0, inplace=True)
        else:
            df[col].fillna('', inplace=True)
    return df

def clean_nulls_json(data: list) -> list:
    """
    Cleans a list of JSON/dict objects by removing entries with missing 'text'
    and filling missing metadata with empty dict
    """
    cleaned = []
    for item in data:
        if not item:
            continue
        text = item.get("text") if isinstance(item, dict) else str(item)
        if not text:
            continue
        meta = item.get("meta", {}) if isinstance(item, dict) else {}
        cleaned.append({"text": text.strip(), "meta": meta})
    return cleaned

def load_csv(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    df = pd.read_csv(file_path)
    return clean_nulls_dataframe(df)

def load_json(file_path: str) -> list:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return clean_nulls_json(data)

if __name__ == "__main__":
    # Example usage for CSV
    csv_path = "data/sample.csv"
    if os.path.exists(csv_path):
        df = load_csv(csv_path)
        print(df.head())

    # Example usage for JSON
    json_path = "data/sample.json"
    if os.path.exists(json_path):
        data = load_json(json_path)
        print(data[:5])
