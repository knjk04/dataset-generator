import logging
import sys
from enum import Enum

import pandas as pd
from dotenv import dotenv_values
from io import StringIO
import openai

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
FORMAT = "%(asctime)s %(message)s"
logger = logging.getLogger()


class Models(Enum):
    # Important for GPT-3.5 to be at the top because this is the default model
    GPT_3_5 = "gpt-3.5-turbo"
    DAVINCI = "text-davinci-003"


def get_response(dataset_of: str, gpt_choice) -> pd.DataFrame:
    env = dotenv_values(".env")
    openai.api_key = env["OPENAI_API_KEY"]

    if gpt_choice == Models.GPT_3_5.value:
        answer = get_gpt_3_5_response(dataset_of)
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


def get_models() -> list[str]:
    return [m.value for m in Models]


get_response("POTUS", "")
