import pandas as pd
import streamlit as st

@st.cache_data
def df_to_csv(df: pd.DataFrame):
    # cache to avoid reconverting on every run
    return df.to_csv().encode("utf-8")


def df_to_json(df: pd.DataFrame):
    # cache to avoid reconverting on every run
    return df.to_json().encode("utf-8")
