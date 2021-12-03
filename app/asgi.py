# -*- coding: utf-8 -*-
"""Application Asynchronous Server Gateway Interface."""
import asyncio
import logging

from app.Models import Users, Courses
from fastapi import FastAPI

from app.Config.routes import router_auth, router_ready, router_courses, router_user
from app.Config.application import (
    DEBUG,
    PROJECT_NAME,
    VERSION
)

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
  cloud_name="hqndlzoag",
  api_key="585514832173685",
  api_secret="ZEND6qDYgV-H6rQEJRp931vS-dw"
)

from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger(__name__)


def get_app():
    """Initialize FastAPI application.

    Returns:
        app (FastAPI): Application object instance.

    """
    log.debug("Initialize FastAPI application node.")

    from app.Config.database import engine
    Users.Base.metadata.create_all(bind=engine)
    Courses.Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=PROJECT_NAME,
        debug=DEBUG,
        version=VERSION,
        docs_url="/swagger",
    )

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    log.debug("Add application routes.")
    app.include_router(router_auth)
    app.include_router(router_ready)
    app.include_router(router_courses)
    app.include_router(router_user)
    return app


application = get_app()
