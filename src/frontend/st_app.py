import streamlit as st
import time

from src.api.process import get_response, get_models
from src.frontend.util import df_to_csv, df_to_json

app_title = "Dataset Generator"
st.set_page_config(page_title=app_title)
st.title(app_title)


def show_export_buttons():
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


def show_result():
    st.dataframe(df, use_container_width=True)
    show_export_buttons()


# TODO: create a numerical box asking for the number of rows
with st.form("form"):
    dataset_entered = st.text_input(label="What would you like a dataset of?", placeholder="E.g. Harry Potter quotes")

    # Manual line breaks are needed because this uses markdown format
    tooltip = """
    We recommend using GPT 3.5.

    GPT 3.5 is newer and more capable. Its training data goes up to Sep 2021.

    Da Vinci's training data only goes up to Oct 2019.
    """

    gpt_choice = st.radio("Which GPT model would you like to use?", get_models(), help=tooltip)

    # TODO: only allow the generate button to be enabled if the user input field is not empty
    # trigger submit when return key is pressed
    generate_clicked = st.form_submit_button(label="Generate dataset", disabled=False)

if generate_clicked:
    if dataset_entered:
        # Show spinner until a DataFrame is returned
        with st.spinner(f"Generating a dataset of {dataset_entered}..."):
            df = get_response(dataset_entered, gpt_choice)
            # the truth value odf a DataFrame is ambiguous, so cannot use  'while not df'
            while df is None:
                # check every 1 second
                time.sleep(1)

        if df.empty:
            st.error(f"We could not generate a {dataset_entered} dataset. Try generating a different dataset.",
                     icon="🤔")
        else:
            show_result()
    else:
        st.error(f"Please enter the dataset you would like us to generate (e.g. 'Harry Potter quotes') dataset.",
                 icon="🥸")
