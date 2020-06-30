FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gettext python3-dev libpq-dev

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system --deploy

COPY . /app

COPY ./compose/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh
