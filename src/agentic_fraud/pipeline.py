from pathlib import Path

import pandas as pd

from .data import load_transactions
from .models import RiskResult
from .rag import RulebookRetriever
from .scoring import RiskScorer


class FraudPipeline:
    def __init__(self, csv_path: str | Path, rulebook_pdf_path: str | Path):
        self.csv_path = Path(csv_path)
        self.rulebook_pdf_path = Path(rulebook_pdf_path)
        self.retriever = RulebookRetriever(self.rulebook_pdf_path)
        self.scorer = RiskScorer(retriever=self.retriever)
        self.df: pd.DataFrame | None = None

    def bootstrap(self) -> None:
        self.df = load_transactions(self.csv_path)
        self.scorer.fit(self.df)

    def score_transaction(self, transaction: dict) -> RiskResult:
        return self.scorer.score_one(transaction)

    def score_all(self) -> list[RiskResult]:
        if self.df is None:
            self.bootstrap()
        assert self.df is not None
        return [self.scorer.score_one(row.to_dict()) for _, row in self.df.iterrows()]

