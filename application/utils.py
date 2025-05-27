import pandas as pd

def checagem_data(df):
    if pd.api.types.is_datetime64_any_dtype(df["data"]):
        df["data"] = df["data"].dt.strftime('%d/%m/%Y')
    df["data"] = df["data"].astype(str)
    return df
