# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, SecretStr, root_validator
from pydantic.tools import parse_obj_as


class Settings(BaseSettings):
    mora_url: AnyHttpUrl = parse_obj_as(AnyHttpUrl, "https://morademo.magenta.dk/")
    saml_token: Optional[UUID] = None

    # Keycloak settings
    auth_server: Optional[AnyHttpUrl] = None
    auth_realm: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    sd_username: str
    sd_password: SecretStr
    sd_institution: str
    sd_base_url: HttpUrl = parse_obj_as(HttpUrl, "https://service.sd.dk/sdws/")
    sd_too_deep: List[str] = []

    @root_validator
    def all_keycloak_settings_must_be_set_if_client_secret_is_set(
        cls, values: Dict[str, Any]
    ):
        if values["client_secret"] is not None and values["saml_token"] is not None:
            raise ValueError("SAML and OIDC cannot be used simultaneously")
        if values["client_secret"] is not None:
            mandatory_settings = ("auth_server", "auth_realm", "client_id")
            missing_settings = tuple(
                filter(lambda setting: values.get(setting) is None, mandatory_settings)
            )

            if missing_settings:
                raise ValueError(
                    "The following ENVs are missing: " + ", ".join(missing_settings)
                )

        return values


def get_settings(**overrides) -> Settings:
    return Settings(**overrides)
