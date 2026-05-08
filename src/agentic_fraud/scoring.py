import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from .models import RiskResult
from .rag import RulebookRetriever
from .rules import apply_rules


def _risk_level(score: float) -> str:
    if score >= 75:
        return "CRITICAL"
    if score >= 55:
        return "HIGH"
    if score >= 35:
        return "MEDIUM"
    return "LOW"


class RiskScorer:
    def __init__(self, retriever: RulebookRetriever | None = None):
        self.retriever = retriever
        self.model = IsolationForest(contamination=0.18, random_state=42)

    def fit(self, transactions: pd.DataFrame) -> None:
        features = transactions[["amount_usd"]].copy()
        features["hour"] = transactions["timestamp"].dt.hour
        self.model.fit(features)

    def score_one(self, transaction: dict) -> RiskResult:
        base_score, reasons = apply_rules(transaction)
        features = pd.DataFrame(
            [
                {
                    "amount_usd": float(transaction["amount_usd"]),
                    "hour": pd.to_datetime(transaction["timestamp"]).hour,
                }
            ]
        )
        anomaly_raw = float(-self.model.score_samples(features)[0])
        anomaly_score = min(35.0, anomaly_raw * 30.0)
        final_score = min(100.0, round(base_score + anomaly_score, 2))
        query = f"{transaction['transaction_type']} {transaction['country']} {transaction.get('risk_flag', '')}"
        retrieved = self.retriever.retrieve(query) if self.retriever else []
        if anomaly_score >= 20:
            reasons.append("Behavioral anomaly score exceeds threshold.")
        if not reasons:
            reasons.append("No substantial rule or anomaly signals detected.")
        return RiskResult(
            transaction_id=str(transaction["transaction_id"]),
            account_id=str(transaction["account_id"]),
            risk_score=final_score,
            risk_level=_risk_level(final_score),
            reasons=reasons,
            anomaly_score=round(anomaly_score, 2),
            retrieved_policies=retrieved,
            metadata={
                "country": transaction["country"],
                "transaction_type": transaction["transaction_type"],
                "amount_usd": float(transaction["amount_usd"]),
            },
        )
