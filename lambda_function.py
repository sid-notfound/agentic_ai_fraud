from pathlib import Path

from src.agentic_fraud.pipeline import FraudPipeline

BASE_DIR = Path(__file__).resolve().parent
pipeline = FraudPipeline(
    csv_path=BASE_DIR / "fraud_aml_poc_transactions.csv",
    rulebook_pdf_path=BASE_DIR / "Rulebook.pdf",
)
pipeline.bootstrap()


def handler(event, context):
    transaction = event.get("transaction")
    if not transaction:
        return {"statusCode": 400, "body": {"error": "Missing 'transaction' payload."}}
    result = pipeline.score_transaction(transaction)
    return {"statusCode": 200, "body": result.model_dump()}

