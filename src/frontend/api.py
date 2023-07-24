import ast
import logging
from enum import Enum
from typing import List

import requests

from io import StringIO

import openai
import pandas as pd


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


def get_gpt_3_5_response(dataset_of: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # Have to say 'make' not 'generate' for GPT 3.5 to work
            {"role": "user", "content": f"Make a markdown table of {dataset_of}"}
        ]
    )
    return response.choices[0].message.content


def get_da_vinci_response(dataset_of: str) -> str:
    response = openai.Completion.create(
        model=Models.DAVINCI.value,
        prompt=f"Generate a markdown table of {dataset_of}",
        max_tokens=4000,
        temperature=0.2,
    )
    logger.debug(f"Tokens used: {response.usage.total_tokens}")
    return response.choices[0].text


def get_auth_header(api_key: str):
    return {
        "Authorization": api_key
    }


def get_response(dataset_of: str, gpt_choice, api_key: str) -> pd.DataFrame:
    headers = get_auth_header(api_key)
    if gpt_choice == Models.GPT_3_5.value:
        url = f"{BASE_URL}/gpt-3.5/{dataset_of}"
        response = requests.get(url=url, headers=headers)
        answer = response.text
    else:
        answer = get_da_vinci_response(dataset_of)
    print(answer)

    data = StringIO(answer)
    df = pd.read_csv(data, sep="|")

    # TODO: add a function that checks if the response is valid markdown

    # The separator also appears at the end, so delete the last redundant column
    df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

    # Remove any unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # We remove the first row because it contains the markdown divider ("----")
    return df.iloc[1:]
