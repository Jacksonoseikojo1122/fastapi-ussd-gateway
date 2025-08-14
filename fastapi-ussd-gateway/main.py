# FastAPI USSD Gateway — by Jackson Kojo Osei
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

app = FastAPI(title="USSD Gateway")

# Simple in-memory session store (replace with Redis in prod)
SESSIONS = {}

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd(
    sessionId: str = Form(...),
    phoneNumber: str = Form(...),
    serviceCode: str = Form(""),
    text: str = Form(""),
):
    # Parse user input
    user_input = text.split("*") if text else []
    step = len(user_input)

    # Start session
    if sessionId not in SESSIONS:
        SESSIONS[sessionId] = {"msisdn": phoneNumber}

    # Flow
    if step == 0 or text == "":
        return "CON Welcome Jackson!\n1. Register\n2. Check Balance\n3. Exit"
    choice = user_input[0]

    if choice == "1":
        if step == 1:
            return "CON Enter your full name:"
        if step == 2:
            SESSIONS[sessionId]["name"] = user_input[1]
            return "CON Enter your city:"
        if step == 3:
            SESSIONS[sessionId]["city"] = user_input[2]
            return f"END Registered {SESSIONS[sessionId]['name']} in {SESSIONS[sessionId]['city']}"
    elif choice == "2":
        # Demo balance
        return "END Balance: GHS 42.50"
    return "END Goodbye"