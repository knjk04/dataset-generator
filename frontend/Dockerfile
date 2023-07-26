FROM python:3.11.4-slim-bookworm

# Streamlit cannot run from the root directory
WORKDIR /app

RUN apt-get update && apt-get install -y  \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Listen on Streamlit's default port
EXPOSE 8501

COPY src /app/frontend/src

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["python3", "-m", "streamlit", "run", "frontend/src/st_app.py", \
            "--server.port=8501", "--server.address=0.0.0.0", \
            "--", "--docker"]
