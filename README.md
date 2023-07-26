![Dataset generator screenshot](docs/readme-feature-image.png)

<p align="center">
    <img src="https://img.shields.io/badge/semantic_release-conventional_commits-e10079?logo=semantic-release" alt="Conventional commits badge"/>
</p>

A Streamlit web app that generates datasets using GPT models.

Features:
- Choose between GPT 3.5 Turbo and text-davinci-003
- Export dataset to CSV

Note: the "text-davinci-002", "davinci" and "curie" models will not be supported as they don't perform as well for this
use case

## Running locally:

Prerequisites:
- Docker
   - Windows or macOS: install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Linux: install [Docker Engine](https://docs.docker.com/engine/) and [Docker Compose](https://docs.docker.com/compose/)

1. In the root of the project, build the images: `docker-compose build`
1. Run the services: `docker-compose up`
1. Go to `http://localhost:8501/` to access the frontend.

## Configure development environment:
1. Run `pip install -r requirements-dev.txt`
1. Install pre-commit hook: `pre-commit install`
1. (Optional) run hook: `pre-commit run --all-files`

PyCharm:
Mark the `src` directory as sources root:
![PyCharm sources root](docs/pycharm.png)

To do this, go to Settings > Project > Project Structure. Then, click on the `src` folder. Finally, click on the
blue Sources button.

# Disclaimer

The quality of the datasets generated depend on the responses by OpenAI GPT models. Consequently, they may not be
factually correct. Please corroborate any data generated with factual sources.
