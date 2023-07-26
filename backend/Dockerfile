FROM python:3.11.4

WORKDIR /src

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src .

# Setting the host makes the server available outside the container
CMD ["python3", "-m", "flask", "run", "--port=8000", "--host=0.0.0.0"]
