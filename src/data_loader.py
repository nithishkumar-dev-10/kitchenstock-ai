import yaml
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def load_data():
    config_path = BASE_DIR / "config" / "config.yaml"


    if not config_path.exists():
        raise FileNotFoundError(
            f"config.yaml not found at {config_path}. "
            "Copy config.example.yaml to config.yaml."
        )

    
    with open(config_path) as f:
        config = yaml.safe_load(f)

  
    if "dataset" not in config or "path" not in config["dataset"]:
        raise KeyError("config.yaml must contain 'dataset.path'")

    data_path = BASE_DIR / config["dataset"]["path"]


    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")

 
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        raise ValueError(f"Error reading dataset: {e}")

    return df, config