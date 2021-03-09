# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

import sys

sys.path.insert(0, "/")
import json
from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from os2mo_http_trigger_protocol import (
    EventType,
    MOTriggerPayload,
    MOTriggerRegister,
    RequestType,
)
from structlog import get_logger

from app.config import get_settings
from app.models import MOSDToolPayload
from app.tracing import setup_instrumentation, setup_logging

logger = get_logger()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    settings = get_settings().dict()

    settings_mapping = {
        "crontab.SAML_TOKEN": "saml_token",
        "mora.base": "mora_url",
        "integrations.SD_Lon.sd_user": "sd_username",
        "integrations.SD_Lon.sd_password": "sd_password",
        "integrations.SD_Lon.base_url": "sd_base_url",
        "integrations.SD_Lon.institution_identifier": "sd_institution",
    }
    dipex_settings = {
        dipex_key: str(settings[app_key])
        for dipex_key, app_key in settings_mapping.items()
        if settings[app_key] is not None
    }
    print(dipex_settings)

    settings_path = "/opt/os2mo-data-import-and-export/settings/settings.json"
    with open(settings_path, "w") as settings_file:
        json.dump(dipex_settings, settings_file)


def fix_departments(uuid: UUID):
    import os
    import subprocess

    os.environ["SCRIPT_NAME"] = "/sdtool"
    script = ["/app/update_unit.sh"]
    script.append(str(uuid))

    try:
        logger.info("Running script", command=script)
        result = subprocess.run(
            script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        result.check_returncode()
    except OSError as e:
        logger.exception("Script error occurred", exc=e)
        raise HTTPException(detail={"error": str(e)}, status_code=500)
    except subprocess.CalledProcessError as e:
        logger.exception("Script error occurred", exc=e)
        print(e.stdout.decode("utf-8"))
        raise HTTPException(detail={"error": str(e)}, status_code=500)
    return {"output": result.stdout.decode("utf-8").strip()}


@app.get(
    "/triggers",
    tags=["Trigger API"],
    summary="List triggers to be registered.",
    response_model=List[MOTriggerRegister],
    response_description=(
        "Successful Response" + "<br/>" + "List of triggers to register."
    ),
)
def triggers():
    """List triggers to be registered."""
    return [
        {
            "event_type": EventType.ON_BEFORE,
            "request_type": RequestType.REFRESH,
            "role_type": "org_unit",
            "url": "/triggers/ou/refresh",
        }
    ]


@app.post(
    "/triggers/ou/refresh",
    tags=["Trigger API"],
    summary="Update the specified MO unit according to SD data",
    response_model=Dict[str, str],
    response_description=("Successful Response" + "<br/>" + "Script output."),
)
async def triggers_ou_refresh(payload: MOTriggerPayload):
    """Update the specified MO unit according to SD data"""
    return fix_departments(payload.request["uuid"])


@app.post(
    "/",
    tags=["Old SDTool API"],
    summary="Update the specified MO unit according to SD data",
    response_model=Dict[str, str],
    response_description=("Successful Response" + "<br/>" + "Script output."),
)
def oldendpoint(payload: MOSDToolPayload):
    """Update the specified MO unit according to SD data"""
    return fix_departments(payload.uuid)


app = setup_instrumentation(app)
setup_logging()
