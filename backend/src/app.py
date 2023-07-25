from enum import Enum

import openai
from flask import Flask, abort, request

from .error_messages import ErrorMessages
from .http_status_codes import StatusCodes

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
        abort(StatusCodes.UNAUTHORISED.value, ErrorMessages.NO_API_KEY.value)

    try:
        response = openai.ChatCompletion.create(
            model=Models.GPT_3_5.value,
            messages=[
                {
                    "role": "user",
                    # Have to say 'make' not 'generate' for GPT 3.5 to work
                    "content": f"Make a markdown table of {dataset}"
                }
            ]
        )
        return response.choices[0].message.content
    except openai.error.RateLimitError:
        abort(
            StatusCodes.BAD_REQUEST.value,
            ErrorMessages.RATE_LIMIT.value
        )
    except openai.error.AuthenticationError:
        abort(
            StatusCodes.UNAUTHORISED.value,
            ErrorMessages.INVALID_API_KEY.value
        )


@app.route("/davinci/<dataset>")
def get_davinci_response(dataset: str) -> str:
    openai.api_key = request.headers.get("Authorization")
    if not openai.api_key:
        abort(StatusCodes.UNAUTHORISED.value, ErrorMessages.NO_API_KEY.value)

    try:
        response = openai.Completion.create(
            model=Models.DAVINCI.value,
            prompt=f"Generate a markdown table of {dataset}",
            max_tokens=4000,
            temperature=0.2,
        )
        return response.choices[0].text
    except openai.error.RateLimitError:
        abort(
            StatusCodes.BAD_REQUEST.value,
            ErrorMessages.RATE_LIMIT.value
        )
    except openai.error.AuthenticationError:
        abort(StatusCodes.UNAUTHORISED.value,
              ErrorMessages.INVALID_API_KEY.value)


if __name__ == '__main__':
    # Streamlit runs on port 5000 by default, so use a different port
    app.run(port=8000)
