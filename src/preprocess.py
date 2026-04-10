import pandas as pd

REQUIRED_COLS = ["id", "name", "quantity"]

def validate_schema(df):
    if not all(col in df.columns for col in REQUIRED_COLS):
        raise ValueError(f"Missing required columns: {REQUIRED_COLS}")

def clean_data(df):
    df = df.copy()

    df.columns = df.columns.str.lower().str.strip()

   
    df = df.drop_duplicates()

    
    df = df.dropna(subset=["id", "name", "quantity"])


    df["name"] = df["name"].astype(str).str.lower().str.strip()

   
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")


    df = df.dropna(subset=["quantity"])
    df["quantity"] = df["quantity"].astype(int)

    return df