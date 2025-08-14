# FastAPI USSD Gateway
Implements a classic aggregator flow using `CON`/`END` responses and simple session memory.

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```
## Test (simulate)
```
curl -X POST http://127.0.0.1:8001/ussd -d "sessionId=abc&phoneNumber=+233201234567&text="
curl -X POST http://127.0.0.1:8001/ussd -d "sessionId=abc&phoneNumber=+233201234567&text=1"
curl -X POST http://127.0.0.1:8001/ussd -d "sessionId=abc&phoneNumber=+233201234567&text=1*Jackson"
curl -X POST http://127.0.0.1:8001/ussd -d "sessionId=abc&phoneNumber=+233201234567&text=1*Jackson*Kumasi"
```