from enum import Enum

from flask import Flask

app = Flask(__name__)


class Models(Enum):
    # Important for GPT-3.5 to be at the top because this is the default model
    GPT_3_5 = "gpt-3.5-turbo"
    DAVINCI = "text-davinci-003"


@app.route("/models")
def get_models() -> list[str]:
    return [m.value for m in Models]


if __name__ == '__main__':
    app.run(port=8000)
