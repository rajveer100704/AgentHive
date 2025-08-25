import logging
import os

def initialize_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, "agenthive.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("Logging initialized")

def greet(name: str) -> str:
    return f"Hello, {name}!"

def load_config(path: str):
    """Load configuration from file"""
    import json
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

