from pathlib import Path

from fastapi import FastAPI

from src.agentic_fraud.models import RiskResult, Transaction
from src.agentic_fraud.pipeline import FraudPipeline

BASE_DIR = Path(__file__).resolve().parent
pipeline = FraudPipeline(
    csv_path=BASE_DIR / "fraud_aml_poc_transactions.csv",
    rulebook_pdf_path=BASE_DIR / "Rulebook.pdf",
)
pipeline.bootstrap()

app = FastAPI(title="Agentic AI Fraud & AML", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/score", response_model=RiskResult)
def score_transaction(transaction: Transaction) -> RiskResult:
    return pipeline.score_transaction(transaction.model_dump())


@app.get("/score-all", response_model=list[RiskResult])
def score_all() -> list[RiskResult]:
    return pipeline.score_all()

