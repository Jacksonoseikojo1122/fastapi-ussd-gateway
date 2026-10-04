"""HTTP layer for the Demo Wallet USSD gateway (Africa's Talking-style callback)."""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

from menu import handle

app = FastAPI(title="FastAPI USSD Gateway")

OptionalField = Annotated[str | None, Form()]


@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "ok"


@app.post("/ussd", response_class=PlainTextResponse)
def ussd(
    sessionId: OptionalField = None,  # noqa: N803 - field names are fixed by the protocol
    phoneNumber: OptionalField = None,  # noqa: N803
    serviceCode: OptionalField = None,  # noqa: N803
    text: OptionalField = None,
) -> PlainTextResponse:
    # Required fields are checked here (rather than with Form(...)) so a bad
    # request gets a plain-text 400, not FastAPI's default JSON 422.
    missing = [
        name
        for name, value in (("sessionId", sessionId), ("phoneNumber", phoneNumber))
        if value is None or not value.strip()
    ]
    if missing:
        return PlainTextResponse(
            f"Missing required field(s): {', '.join(missing)}", status_code=400
        )

    return PlainTextResponse(handle(text or ""))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
