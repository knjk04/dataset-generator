import ast
import logging
from enum import Enum
from io import StringIO
from typing import List

import openai
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8000"

logger = logging.getLogger(__name__)
# Set other loggers to error to not clutter this app's logs
logging.basicConfig(level=logging.ERROR)
logging.getLogger(__name__).setLevel(logging.DEBUG)


def get_models() -> List[str]:
    r = requests.get(f"{BASE_URL}/models")
    # TODO: show error message if status not 200 OK
    return ast.literal_eval(r.text)


class Models(Enum):
    # Important for GPT-3.5 to be at the top because this is the default model
    GPT_3_5 = "gpt-3.5-turbo"
    DAVINCI = "text-davinci-003"


def get_auth_header(api_key: str):
    return {
        "Authorization": api_key
    }


def get_response(dataset_of: str, gpt_choice, api_key: str) -> pd.DataFrame:
    if gpt_choice == Models.GPT_3_5.value:
        url = f"{BASE_URL}/gpt-3.5/{dataset_of}"
    else:
        url = f"{BASE_URL}/davinci/{dataset_of}"

    headers = get_auth_header(api_key)
    response = requests.get(url=url, headers=headers)
    return str_to_df(response.text)


# TODO: add a function that checks if the input is valid markdown
def str_to_df(s: str) -> pd.DataFrame:
    data = StringIO(s)
    df = pd.read_csv(data, sep="|")

    # The separator is also at the end, so delete the last redundant column
    df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

    # Remove any unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # We remove the first row because it contains the markdown divider ("----")
    return df.iloc[1:]
