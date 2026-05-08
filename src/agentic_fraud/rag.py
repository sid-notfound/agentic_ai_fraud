from pathlib import Path

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RulebookRetriever:
    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)
        self.chunks = self._load_chunks()
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.chunks) if self.chunks else None

    def _load_chunks(self) -> list[str]:
        if not self.pdf_path.exists():
            return []
        pages: list[str] = []
        reader = PdfReader(str(self.pdf_path))
        for page in reader.pages:
            text = page.extract_text() or ""
            text = " ".join(text.split())
            if text:
                pages.append(text)
        return pages

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        if not self.chunks or self.matrix is None:
            return []
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.matrix).flatten()
        top_indices = sims.argsort()[::-1][:top_k]
        return [self.chunks[i][:350] for i in top_indices if sims[i] > 0]

