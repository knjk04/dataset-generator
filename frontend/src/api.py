import ast
import logging
from enum import Enum
from io import StringIO
from typing import List

import bs4
import pandas as pd
import requests
from requests.exceptions import HTTPError

from frontend.src.server_exception import ServerException

logger = logging.getLogger(__name__)
# Set other loggers to error to not clutter this app's logs
logging.basicConfig(level=logging.ERROR)
logging.getLogger(__name__).setLevel(logging.DEBUG)


def get_base_url(host: str) -> str:
    return f"{host}:8000"


def get_models(host) -> List[str]:
    r = requests.get(f"{get_base_url(host)}/models")
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


def get_response(dataset_of: str, gpt_choice, api_key: str,
                 host: str) -> pd.DataFrame:
    base_url = get_base_url(host)
    if gpt_choice == Models.GPT_3_5.value:
        url = f"{base_url}/gpt-3.5/{dataset_of}"
    else:
        url = f"{base_url}/davinci/{dataset_of}"

    headers = get_auth_header(api_key)

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        status_code = response.status_code
        if status_code == 200:
            return str_to_df(response.text)
    except HTTPError as e:
        html = bs4.BeautifulSoup(e.response.text, features="html.parser")
        server_message = html.p.text
        logger.info(server_message)
        raise ServerException(server_message)


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
