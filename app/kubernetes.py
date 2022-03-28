# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
from httpx import AsyncClient
from httpx import HTTPError
from fastapi import APIRouter
from fastapi import Response
from starlette.status import HTTP_204_NO_CONTENT
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE

from app.config import get_settings

_settings = get_settings()
_url = f"{_settings.sd_base_url}/GetPerson20111201"
_query_params = {"InstitutionIdentifier": _settings.sd_institution}
_auth = (_settings.sd_username, _settings.sd_password)

kubernetes_router = APIRouter()


@kubernetes_router.get("/live", status_code=HTTP_204_NO_CONTENT)
async def liveness():
    """
    Endpoint to be used as a liveness probe for Kubernetes
    """
    return


@kubernetes_router.get("/ready", status_code=HTTP_204_NO_CONTENT)
async def readiness(response: Response):
    """
    Endpoint to be used as a readiness probe for Kubernetes.
    If SDTool is capable of calling SD Løn and get XML back,
    it is considered to be ready.
    """

    async with AsyncClient() as client:
        try:
            r = await client.get(_url, params=_query_params, auth=_auth)
            r.raise_for_status()
        except HTTPError:
            response.status_code = HTTP_503_SERVICE_UNAVAILABLE

    content_type_header = r.headers.get("content-type")
    content_type = content_type_header.split(";")[0]
    if not content_type == "text/xml":
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
