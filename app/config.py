# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
from typing import Optional, List
from uuid import UUID

from pydantic import BaseSettings, HttpUrl
from pydantic.tools import parse_obj_as

from app.pydantic_types import Domain, Port


class Settings(BaseSettings):
    mora_url: HttpUrl = parse_obj_as(HttpUrl, "https://morademo.magenta.dk/")
    saml_token: Optional[UUID] = None

    sd_username: str
    sd_password: str
    sd_institution: str
    sd_base_url: HttpUrl = parse_obj_as(HttpUrl, "https://service.sd.dk/sdws/")
    sd_too_deep: List[str] = []

    jaeger_service: str = "TriggerExample"
    jaeger_hostname: Optional[Domain] = None
    jaeger_port: Port = Port(6831)


def get_settings(**overrides) -> Settings:
    return Settings(**overrides)
