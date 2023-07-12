import ast
from typing import List
import requests

BASE_URL = "http://127.0.0.1:8000"


def get_models() -> List[str]:
    r = requests.get(f"{BASE_URL}/models")
    # TODO: show error message if status not 200 OK
    return ast.literal_eval(r.text)

