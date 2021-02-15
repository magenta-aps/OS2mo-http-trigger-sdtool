FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt

WORKDIR /app
COPY ./app /app
