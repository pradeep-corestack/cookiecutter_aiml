from typing import List, Dict

import uvicorn

# from oslo_config import cfg
from fastapi import FastAPI, APIRouter
from core.config.config import ConfigSetup


from loguru import logger

# TODO: {{cookiecutter.author}} rotation to be configurable
logger.add("logs/{}.log".format(__name__), filter=__name__, rotation="1 week")


description = """
Swagger interface for {{cookiecutter.domain_name}}

## External

External APIs are exposed in the public domain for customers

## Internal

APIs internal to {{cookiecuuter.organization}}

"""

tags_metadata = [
    {
        "name": "Internal",
        "description": "Internal APIs for Corestack",
    },
    {
        "name": "External",
        "description": "External API to be exposed to Corestack  customers",
    },
]

app = FastAPI(
    title="{{cookiecutter.domain_name}}",
    description=description,
    version="0.0.1",
    contact={
        "name": "Corestack",
        "url": "http://corestack.io/contact/",
        "email": "{{cookiecutter.email}}",
    },
    openapi_tags=tags_metadata,
)

router = APIRouter()

db = None

from enum import Enum


@router.get(
    "/endpoint",
    tags=["Internal"],
    summary="summary",
)
async def function_name():
    return [{}]


def main():
    app.include_router(router)
    # uvicorn.run(app, host=cfg.CONF.bind_host, port=cfg.CONF.bind_port)
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    ConfigSetup().init()
    main()
