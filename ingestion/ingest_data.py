import os
import json
from ingestion.preprocess import preprocess_data

DATA_DIR = "data/raw"

def ingest_data():
    all_data = []
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".json"):
            with open(os.path.join(DATA_DIR, file_name), "r", encoding="utf-8") as f:
                data = json.load(f)
                all_data.extend(data)
    processed_data = preprocess_data(all_data)
    print(f"Ingested and processed {len(processed_data)} items")
    return processed_data

if __name__ == "__main__":
    ingest_data()

