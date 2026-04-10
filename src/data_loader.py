import pandas as pd
import yaml
from pathlib import Path

# Base directory (root of project)
BASE_DIR = Path(__file__).resolve().parent.parent


def load_config():
    """
    Load configuration file.
    Priority:
    1. config.yaml (local - full mode)
    2. config.example.yaml (fallback - sample mode)
    """

    config_path = BASE_DIR / "config" / "config.yaml"
    example_path = BASE_DIR / "config" / "config.example.yaml"

    if config_path.exists():
        final_config_path = config_path
        print(" Using config.yaml (FULL mode)")
    elif example_path.exists():
        final_config_path = example_path
        print(" Using config.example.yaml (SAMPLE mode)")
    else:
        raise FileNotFoundError(" No config file found!")

    with open(final_config_path) as f:
        config = yaml.safe_load(f)

    return config


def load_data():
    """
    Load dataset based on config
    """

    config = load_config()

    # Validate config structure
    if "dataset" not in config or "path" not in config["dataset"]:
        raise KeyError(" config.yaml must contain 'dataset.path'")

    data_path = BASE_DIR / config["dataset"]["path"]

    if not data_path.exists():
        raise FileNotFoundError(f" Dataset not found at: {data_path}")

    print(f"📂 Loading dataset from: {data_path}")

    df = pd.read_csv(data_path)

    print(f" Data loaded successfully: {df.shape}")

    return df, config