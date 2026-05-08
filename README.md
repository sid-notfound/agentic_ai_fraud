# Agentic AI for Fraud, AML & Financial Crime

Production-style PoC for transaction risk detection with:
- Rule-based AML scoring
- IsolationForest anomaly detection
- RAG retrieval over a compliance rulebook PDF
- Explainable output per transaction
- FastAPI endpoint for real-time scoring
- AWS Lambda-compatible handler

## Tech Stack
- Python
- FastAPI
- scikit-learn
- RAG (TF-IDF retrieval over PDF policy text)
- AWS-ready entrypoint (`lambda_function.py`)
- Compatible with AWS Bedrock / Claude integration paths

## Project Structure
```text
.
├── app.py
├── lambda_function.py
├── scripts/run_demo.py
├── src/agentic_fraud/
│   ├── data.py
│   ├── explain.py
│   ├── models.py
│   ├── pipeline.py
│   ├── rag.py
│   ├── rules.py
│   └── scoring.py
├── tests/test_pipeline.py
├── fraud_aml_poc_transactions.csv
└── Rulebook.pdf
```

## Setup
1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Demo
```bash
python scripts/run_demo.py
```

## Run API (real-time scoring)
```bash
uvicorn app:app --reload --port 8000
```

Endpoints:
- `GET /health`
- `POST /score`
- `GET /score-all`

Example payload for `POST /score`:
```json
{
  "transaction_id": "TXN99999",
  "account_id": "ACC9999",
  "timestamp": "2025-10-01T10:30:00",
  "transaction_type": "Wire Transfer",
  "amount_usd": 28000,
  "country": "Russia",
  "risk_flag": "Structuring"
}
```

## Run Tests
```bash
pytest -q
```

## AWS Lambda
- File: `lambda_function.py`
- Handler: `lambda_function.handler`
- Event shape:
```json
{
  "transaction": {
    "transaction_id": "TXN123",
    "account_id": "ACC123",
    "timestamp": "2025-10-01T12:30:00",
    "transaction_type": "Crypto Transfer",
    "amount_usd": 21000,
    "country": "UAE",
    "risk_flag": "High Velocity"
  }
}
```

## Bedrock / Claude Integration Note
This implementation is model-agnostic. To connect an LLM explainer:
- Set `BEDROCK_MODEL_ID` for AWS Bedrock usage, or
- Set `ANTHROPIC_API_KEY` for Claude API usage,
- Then call your provider in a follow-up explainer service using prompts from `src/agentic_fraud/explain.py`.
