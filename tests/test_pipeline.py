from pathlib import Path

from src.agentic_fraud.pipeline import FraudPipeline


def test_pipeline_scores_transactions():
    base_dir = Path(__file__).resolve().parents[1]
    pipeline = FraudPipeline(
        csv_path=base_dir / "fraud_aml_poc_transactions.csv",
        rulebook_pdf_path=base_dir / "Rulebook.pdf",
    )
    pipeline.bootstrap()
    results = pipeline.score_all()
    assert len(results) > 0
    assert all(0 <= r.risk_score <= 100 for r in results)

