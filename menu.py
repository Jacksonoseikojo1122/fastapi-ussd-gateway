"""Demo Wallet USSD menu.

``handle(text)`` is a pure function: the reply depends only on ``text``, the
'*'-joined history of everything the subscriber has typed this session
(e.g. "" -> "1" -> "1*20" -> "1*20*1"). The aggregator resends the full
history on every hop, so no server-side session state is needed.

Replies start with "CON " (keep the session open) or "END " (close it).
Invalid input ends the session with a message explaining what was expected.
"""

from __future__ import annotations

import re
from decimal import Decimal

MAIN_MENU = (
    "CON Welcome to Demo Wallet\n1. Buy airtime\n2. Register\n3. Check balance\n0. Exit"
)
ENTER_AMOUNT = "CON Enter amount in GHS (1-500):"
INVALID_AMOUNT = (
    "END Invalid amount. Enter a number from 1 to 500 with at most 2 decimal places."
)
PURCHASE_CANCELLED = "END Purchase cancelled."
ENTER_NAME = "CON Enter your full name:"
INVALID_NAME = "END Invalid name. Use 2 to 60 characters."
ENTER_TOWN = "CON Enter your town:"
INVALID_TOWN = "END Invalid town. Use 2 to 40 characters."
GOODBYE = "END Goodbye."
INVALID_OPTION = "END Invalid option."

# Demo value only: a real deployment would query the wallet/ledger service.
DEMO_BALANCE_GHS = "42.50"

AMOUNT_MIN = Decimal("1")
AMOUNT_MAX = Decimal("500")
# re.ASCII limits \d to 0-9, matching JavaScript's \d in the Node twin.
_AMOUNT_PATTERN = re.compile(r"\d+(\.\d{1,2})?", re.ASCII)


def parse_amount(raw: str) -> str | None:
    """Return the amount formatted to 2dp (e.g. "20.00"), or None if invalid."""
    value = raw.strip()
    if not _AMOUNT_PATTERN.fullmatch(value):
        return None
    amount = Decimal(value)
    if not AMOUNT_MIN <= amount <= AMOUNT_MAX:
        return None
    return f"{amount:.2f}"


def _is_valid_length(value: str, minimum: int, maximum: int) -> bool:
    return minimum <= len(value) <= maximum


def _buy_airtime(steps: list[str]) -> str:
    if not steps:
        return ENTER_AMOUNT

    amount = parse_amount(steps[0])
    if amount is None:
        return INVALID_AMOUNT

    if len(steps) == 1:
        return f"CON Buy GHS {amount} airtime?\n1. Confirm\n2. Cancel"
    if len(steps) > 2:
        return INVALID_OPTION

    confirmation = steps[1]
    # Simulated purchase: no payment provider is called in this demo.
    if confirmation == "1":
        return f"END Airtime purchase of GHS {amount} successful."
    if confirmation == "2":
        return PURCHASE_CANCELLED
    return INVALID_OPTION


def _register(steps: list[str]) -> str:
    if not steps:
        return ENTER_NAME

    name = steps[0].strip()
    if not _is_valid_length(name, 2, 60):
        return INVALID_NAME

    if len(steps) == 1:
        return ENTER_TOWN
    if len(steps) > 2:
        return INVALID_OPTION

    town = steps[1].strip()
    if not _is_valid_length(town, 2, 40):
        return INVALID_TOWN

    return f"END Registered {name}, {town}."


def handle(text: str = "") -> str:
    """Return the reply for a '*'-joined input history ("" on the first request)."""
    if text == "":
        return MAIN_MENU

    choice, *steps = text.split("*")
    match choice.strip():
        case "1":
            return _buy_airtime(steps)
        case "2":
            return _register(steps)
        case "3":
            return f"END Balance: GHS {DEMO_BALANCE_GHS}" if not steps else INVALID_OPTION
        case "0":
            return GOODBYE if not steps else INVALID_OPTION
        case _:
            return INVALID_OPTION
