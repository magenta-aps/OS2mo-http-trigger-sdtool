# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

from typing import Optional

from pydantic import BaseSettings

from app.pydantic_types import Domain, Port


class Settings(BaseSettings):
    configured_value: str = "TriggerExample"

    jaeger_service: str = "TriggerExample"
    jaeger_hostname: Optional[Domain] = None
    jaeger_port: Port = Port(6831)


def get_settings(**overrides) -> Settings:
    return Settings(**overrides)
