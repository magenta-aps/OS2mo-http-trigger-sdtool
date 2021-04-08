# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
from typing import List, Optional
from uuid import UUID

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl
from pydantic.tools import parse_obj_as


class Settings(BaseSettings):
    mora_url: HttpUrl = parse_obj_as(AnyHttpUrl, "https://morademo.magenta.dk/")
    saml_token: Optional[UUID] = None

    sd_username: str
    sd_password: str
    sd_institution: str
    sd_base_url: HttpUrl = parse_obj_as(HttpUrl, "https://service.sd.dk/sdws/")
    sd_too_deep: List[str] = []


def get_settings(**overrides) -> Settings:
    return Settings(**overrides)
