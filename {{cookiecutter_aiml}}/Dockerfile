FROM python:3.8-buster
WORKDIR /{{cookiecutter.project_name}}
STOPSIGNAL SIGINT

ENV LISTEN_PORT 9090

# System dependencies
RUN pip3 install poetry

# Project dependencies

# TODO: {{cookiecutter.author}} download from private repo
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-dev

COPY . .

# commented
# RUN python /{{cookiecutter.project_name}}/app/api.py 
