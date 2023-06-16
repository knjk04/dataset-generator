# Dataset Generator

A Streamlit web app that generates datasets using GPT models.

Features:
- Export dataset to CSV

## Running locally:

Prerequisites:
- Python installed (test with Python 3.11)

1. Create a `.env` file in the root directory of the repository
2. Add your OpenAI API key in the .env file.
  - The environment variable should have `OPENAI_API_KEY` as the key name.
  - Example file (not a real API key):
    ```
    OPENAI_API_KEY=ab-0a0aaaaA0aaAAa0AaaaaA00aaaAA0aA0aaA0AaAAaaaaaa00
    ```
3. Install dependencies: `pip install -r src/requirements.txt`
