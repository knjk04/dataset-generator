# Dataset Generator

A Streamlit web app that generates datasets using GPT models.

Features:
- Choose between GPT 3.5 Turbo and text-davinci-003
- Export dataset to CSV

Note: the "text-davinci-002", "davinci" and "curie" models will not be supported as they don't perform as well for this
use case

## Running locally:

Prerequisites:
- Python installed (test with Python 3.11)

Steps:

1. Create a `.env` file in the root directory of the repository
2. Add your OpenAI API key in the .env file.
  - The environment variable should have `OPENAI_API_KEY` as the key name.
  - Example file (not a real API key):
    ```
    OPENAI_API_KEY=ab-0a0aaaaA0aaAAa0AaaaaA00aaaAA0aA0aaA0AaAAaaaaaa00
    ```
3. Install dependencies: `pip install -r src/requirements.txt`
