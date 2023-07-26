import argparse
import time

import pandas as pd
import streamlit as st

from frontend.src.api import get_models, get_response
from frontend.src.server_exception import ServerException
from frontend.src.util import df_to_csv, df_to_json

parser = argparse.ArgumentParser()
parser.add_argument("--docker", action="store_true")
args = parser.parse_args()
if args.docker:
    HOST = "http://backend"
else:
    # local development
    HOST = "http://127.0.0.1"
print(HOST)


app_title = "Dataset Generator"
st.set_page_config(page_title=app_title)
st.title(app_title)


def show_export_buttons(df: pd.DataFrame):
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.download_button(
            label="Export to CSV",
            data=df_to_csv(df),
            file_name="dataset.csv",
            mime="text/csv"
        )
    with col2:
        st.download_button(
            label="Export to JSON",
            data=df_to_json(df),
            file_name="dataset.json",
            mime="application/json"
        )


def show_result(df: pd.DataFrame):
    st.dataframe(df, use_container_width=True)
    show_export_buttons(df)


def get_gpt_radio():
    # Manual line breaks are needed because this uses Markdown format
    tooltip = """
    We recommend using GPT 3.5.

    GPT 3.5 is newer and more capable. Its training data goes up to Sep 2021.

    Da Vinci's training data only goes up to Oct 2019.
    """
    return st.radio("Which GPT model would you like to use?", get_models(HOST),
                    help=tooltip)


# TODO: create a numerical box asking for the number of rows
with st.form("form"):
    api_key = st.text_input("Please enter your OpenAI API key",
                            placeholder="OpenAI API key")

    dataset_entered = st.text_input(label="What would you like a dataset of?",
                                    placeholder="E.g. Harry Potter quotes")

    gpt_choice = get_gpt_radio()

    # TODO: only allow the generate button to be enabled if the user input field is not empty
    # trigger submit when return key is pressed
    generate_clicked = st.form_submit_button(label="Generate dataset",
                                             disabled=False)


def generate_dataset():
    if not api_key:
        st.error(
            f"You did not enter in an API key. Please enter your OpenAI API "
            f"key and try again", icon="🥸"
        )
        return
    if not dataset_entered:
        st.error(
            f"Please enter the dataset you would like us to generate (e.g. "
            f"'Harry Potter quotes') dataset.", icon="🥸"
        )
        return

    # Show spinner until a DataFrame is returned
    with st.spinner(f"Generating a dataset of {dataset_entered}..."):
        try:
            df = get_response(dataset_entered, gpt_choice, api_key, HOST)
            # the truth value of a DataFrame is ambiguous, so cannot use
            # 'while not df'
            while df is None:
                # check every 1 second
                time.sleep(1)
        except ServerException as e:
            st.error(e.message)
            return

    if df.empty:
        st.error(
            f"We could not generate a {dataset_entered} dataset. "
            f"Try generating a different dataset.", icon="🤔"
        )
    else:
        show_result(df)


if generate_clicked:
    generate_dataset()
