import logging
import sys

import pandas as pd
from dotenv import dotenv_values
from io import StringIO
import openai

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
FORMAT = "%(asctime)s %(message)s"
logger = logging.getLogger()


def get_response(dataset_of: str) -> pd.DataFrame:
    env = dotenv_values(".env")
    openai.api_key = env["OPENAI_API_KEY"]

    # TODO: allow users to use a different model
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Generate a table of {dataset_of}",
        max_tokens=4000,
        temperature=0.2,
    )

    logger.debug(f"Tokens used: {response.usage.total_tokens}")
    answer = response.choices[0].text
    print(repr(answer))
    print(answer)
    data = StringIO(answer)
    df = pd.read_csv(data, sep="|")

    # The separator also appears at the end, so delete the last redundant column
    df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

    # TODO: drop unnamed columns

    return df


def get_models() -> list[str]:
    # text - davinci - 003, text - davinci - 002, davinci, curie, babbage, ada
    raise NotImplementedError
