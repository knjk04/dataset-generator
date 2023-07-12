from enum import Enum

import openai
from dotenv import dotenv_values
from flask import Flask

app = Flask(__name__)


class Models(Enum):
    # Important for GPT-3.5 to be at the top because this is the default model
    GPT_3_5 = "gpt-3.5-turbo"
    DAVINCI = "text-davinci-003"


@app.route("/models")
def get_models() -> list[str]:
    return [m.value for m in Models]


@app.route("/gpt-3.5/<dataset>")
def get_gpt_3_5_response(dataset: str) -> str:
    env = dotenv_values(".env")
    openai.api_key = env["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # Have to say 'make' not 'generate' for GPT 3.5 to work
            {"role": "user", "content": f"Make a markdown table of {dataset}"}
        ]
    )
    # TODO: handle rate limit error
    return response.choices[0].message.content


if __name__ == '__main__':
    # Streamlit runs on port 5000 by default, so use a different port
    app.run(port=8000)
