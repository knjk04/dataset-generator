from enum import Enum

import openai
from flask import Flask, request, abort

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
    openai.api_key = request.headers.get("Authorization")
    if not openai.api_key:
        abort(403, "API key not given")
    print("API key: " + openai.api_key)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    # Have to say 'make' not 'generate' for GPT 3.5 to work
                    "content": f"Make a markdown table of {dataset}"
                }
            ]
        )
        # TODO: handle rate limit error
        return response.choices[0].message.content
    except openai.error.AuthenticationError:
        abort (403, "API key given is not valid")


if __name__ == '__main__':
    # Streamlit runs on port 5000 by default, so use a different port
    app.run(port=8000)
