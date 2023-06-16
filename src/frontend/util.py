import pandas as pd


def df_to_csv(df: pd.DataFrame):
    return df.to_csv().encode("utf-8")


def df_to_json(df: pd.DataFrame):
    return df.to_json().encode("utf-8")
