import pandas as pd
import streamlit as st
import time

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
    with st.spinner(f"Generating a dataset of {dataset}..."):
        time.sleep(5)

if generate and dataset:
    df = get_response(dataset)
    # If dataframe is empty, show an error message and hide the download button
    if df.empty:
        st.error(f"We could not generate a {dataset} dataset. Try generating a different dataset.",
                 icon="🤔")
    else:
        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="Export to CSV",
            data=df_to_csv(df),
            file_name="dataset.csv",
            mime="text/csv"
        )
