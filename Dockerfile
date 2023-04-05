FROM python:3.10-slim-buster

WORKDIR /app

# Needed for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    default-mysql-client

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api api
COPY main.py main.py
COPY gunicorn.conf.py gunicorn.conf.py
COPY config.py config.py
COPY data_extractor.py data_extractor.py
COPY test test
COPY txt txt

COPY .docker_env .env

EXPOSE 8000

CMD ["gunicorn", "main:app", "--config", "gunicorn.conf.py"]
