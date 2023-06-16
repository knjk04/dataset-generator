import pandas as pd
import streamlit as st

from process import get_response


def df_to_csv(df: pd.DataFrame):
    return df.to_csv().encode("utf-8")


app_title = "Dataset Generator"
st.set_page_config(page_title=app_title)
st.title(app_title)

# TODO: create a numerical box asking for the number of rows

with st.form("form"):
    # invalid = True
    dataset = st.text_input(label="What would you like a dataset of?", placeholder="E.g. Harry Potter quotes")
    # if dataset:
    #     invalid = False

    # TODO: only allow the generate button to be enabled if the user input field is not empty
    invalid = False
    generate = st.form_submit_button(label="Generate dataset", disabled=invalid)

if dataset:
    st.write(f'Generating a dataset of {dataset}...')

if generate and dataset:
    df = get_response(dataset)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="Export to CSV",
        data=df_to_csv(df),
        file_name="dataset.csv",
        mime="text/csv"
    )


