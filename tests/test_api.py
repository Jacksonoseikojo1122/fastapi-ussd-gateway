import pytest
from fastapi.testclient import TestClient

from main import app

SESSION = {"sessionId": "ATUid_123", "phoneNumber": "+233241234567", "serviceCode": "*384*123#"}


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_full_airtime_purchase_over_http(client):
    hops = [
        ("", "CON Welcome to Demo Wallet\n1. Buy airtime\n2. Register\n3. Check balance\n0. Exit"),
        ("1", "CON Enter amount in GHS (1-500):"),
        ("1*20", "CON Buy GHS 20.00 airtime?\n1. Confirm\n2. Cancel"),
        ("1*20*1", "END Airtime purchase of GHS 20.00 successful."),
    ]
    for text, expected in hops:
        response = client.post("/ussd", data={**SESSION, "text": text})
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain")
        assert response.text == expected


def test_missing_text_is_first_hop(client):
    response = client.post("/ussd", data={"sessionId": "abc", "phoneNumber": "+233201234567"})
    assert response.status_code == 200
    assert response.text.startswith("CON Welcome to Demo Wallet")


def test_missing_session_id_returns_400(client):
    response = client.post("/ussd", data={"phoneNumber": "+233241234567", "text": ""})
    assert response.status_code == 400
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "Missing required field(s): sessionId"


def test_blank_phone_number_returns_400(client):
    response = client.post("/ussd", data={"sessionId": "abc", "phoneNumber": "  ", "text": ""})
    assert response.status_code == 400
    assert response.text == "Missing required field(s): phoneNumber"


def test_empty_body_returns_400(client):
    response = client.post("/ussd")
    assert response.status_code == 400
    assert response.text == "Missing required field(s): sessionId, phoneNumber"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "ok"
