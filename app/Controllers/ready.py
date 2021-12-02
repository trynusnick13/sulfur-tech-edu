import logging

from fastapi import APIRouter
from app.Schemas.ready import ReadyResponse

ready_route = APIRouter()
log = logging.getLogger(__name__)


@ready_route.get(
    '/ready',
    tags=['ready'],
    response_model=ReadyResponse,
    summary="Simple health check."
)
def readiness_check():
    """Run basic application health check.
    Returns:
        response (ReadyResponse): ReadyResponse model object instance.
    """
    log.info("Started GET /ready")
    return ReadyResponse(status="ok")