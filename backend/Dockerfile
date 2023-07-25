FROM python:3.11.4

WORKDIR /src

COPY backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY backend .

CMD ["python3", "-m", "flask", "run", "--port=8000"]
