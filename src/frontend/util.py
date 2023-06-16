import pandas as pd


def df_to_csv(df: pd.DataFrame):
    return df.to_csv().encode("utf-8")
