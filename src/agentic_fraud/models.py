from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    timestamp: datetime
    transaction_type: str
    amount_usd: float
    country: str
    risk_flag: str | None = None


class RiskResult(BaseModel):
    transaction_id: str
    account_id: str
    risk_score: float = Field(ge=0, le=100)
    risk_level: str
    reasons: list[str]
    anomaly_score: float
    retrieved_policies: list[str]
    metadata: dict[str, Any] = Field(default_factory=dict)

