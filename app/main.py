from typing import List

from fastapi import FastAPI
from os2mo_http_trigger_protocol import (EventType, MOTriggerPayload,
                                         MOTriggerRegister, RequestType)

app = FastAPI()


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
            "request_type": RequestType.EDIT,
            "role_type": "org_unit",
            "url": "/triggers/ou/edit",
        }
    ]


@app.post(
    "/triggers/ou/edit",
    summary="Print that an organizational unit has been edited",
)
async def triggers_ou_create(payload: MOTriggerPayload):
    """Fired when an OU has been created."""
    print("OU Edit:", payload)
