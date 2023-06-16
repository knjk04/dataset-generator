import pandas as pd
from dotenv import dotenv_values
from io import StringIO
import openai


# TODO: Take in what dataset the user wants as input and append to prompt
def get_response() -> pd.DataFrame:
    env = dotenv_values(".env")
    openai.api_key = env["OPENAI_API_KEY"]

    # TODO: allow users to use a different model
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate a table of Harry Potter quotes",
        max_tokens=4000,
        temperature=0.2,
    )

    print(f"Tokens used: {response.usage.total_tokens}")
    answer = response.choices[0].text
    print(repr(answer))
    print(answer)
    data = StringIO(answer)
    return pd.read_csv(data, sep="|")
