# {{cookiecutter.project_name}}


## Set PYTHONPATH 

Set `PYTHONPATH` env variable to current project directory
on linux environment

```shell
export PYTHONPATH="."
``

## Install poetry

`pip install poetry`


### Contributing
Run `poetry install` to install the env.

Run `poetry run pre-commit install` to initialize the git hooks.

Run `poetry run pre-commit run --all-files` if there are file that were committed before adding the git hooks.

Activate the shell with: `poetry shell`

## Architecture

![block diagram](./assets/model_training.png)
