import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from src.agentic_fraud.pipeline import FraudPipeline

pipeline = FraudPipeline(
    csv_path=BASE_DIR / "fraud_aml_poc_transactions.csv",
    rulebook_pdf_path=BASE_DIR / "Rulebook.pdf",
)
pipeline.bootstrap()

results = pipeline.score_all()

top = sorted(results, key=lambda r: r.risk_score, reverse=True)[:5]
print("Top 5 highest-risk transactions:")
for row in top:
    print(
        f"{row.transaction_id} | {row.account_id} | {row.risk_level} ({row.risk_score}) | "
        f"Reasons: {', '.join(row.reasons[:2])}"
    )
