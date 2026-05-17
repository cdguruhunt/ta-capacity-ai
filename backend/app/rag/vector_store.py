"""
RAG Vector Store using ChromaDB for TalentScale AI.
Used to retrieve relevant workforce planning context for AI responses.
"""
import os
from typing import List, Dict

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

# Placeholder benchmark documents for RAG ingestion
BENCHMARK_DOCUMENTS = [
    {
        "id": "doc_001",
        "text": "IT Product company recruiters in India close 25–38 hires per year. Niche AI/ML roles reduce productivity by 25–35% due to passive talent, multi-round interviews, and competitive market.",
        "metadata": {"category": "benchmark", "company_type": "product"}
    },
    {
        "id": "doc_002",
        "text": "IT Consulting companies in India operate on volume hiring. Recruiters close 45–65 hires/year. Mass lateral hiring for Java, .NET, Python roles with repeat skill requirements.",
        "metadata": {"category": "benchmark", "company_type": "consulting"}
    },
    {
        "id": "doc_003",
        "text": "Global Capability Centers (GCCs) require a hybrid TA model. Average 30–42 hires/recruiter/year. High complexity for digital transformation roles: data engineering, cloud, DevSecOps.",
        "metadata": {"category": "benchmark", "company_type": "gcc"}
    },
    {
        "id": "doc_004",
        "text": "Recruiter team composition best practice: 40% junior recruiters, 35% mid-level, 25% senior for product companies. For consulting: 50% junior, 35% mid, 15% senior.",
        "metadata": {"category": "team_structure", "company_type": "all"}
    },
    {
        "id": "doc_005",
        "text": "Dropout ratio in Indian tech hiring averages 20–30% for lateral roles. Offer-to-join dropout is highest for FAANG-competitive companies (30–45%) and lowest for PSU/government-adjacent enterprises (5–10%).",
        "metadata": {"category": "dropout", "company_type": "all"}
    },
    {
        "id": "doc_006",
        "text": "TA team operating costs in India: Junior recruiter CTC ₹4–8L/yr, Mid recruiter ₹8–15L/yr, Senior recruiter ₹15–25L/yr, TA Lead ₹20–35L/yr, TA Manager ₹35–55L/yr, TA Head ₹60–120L/yr.",
        "metadata": {"category": "cost", "company_type": "all"}
    },
    {
        "id": "doc_007",
        "text": "Time-to-fill benchmarks India 2024: SDE-1 30 days, SDE-2 45 days, Staff Engineer 70 days, Principal 90 days, AI/ML Specialist 95 days, Data Scientist 80 days.",
        "metadata": {"category": "timeline", "company_type": "product"}
    },
    {
        "id": "doc_008",
        "text": "Sourcing strategy for AI/niche hiring: LinkedIn Premium (40% of sourcing), Naukri database (30%), GitHub/Kaggle active outreach (20%), referrals (10%). Each AI role requires 3x more sourcing touchpoints.",
        "metadata": {"category": "sourcing", "company_type": "product"}
    },
]


class VectorStore:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.available = CHROMA_AVAILABLE
        self.collection = None

        if self.available:
            try:
                self.client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=persist_dir,
                    anonymized_telemetry=False
                ))
                self.collection = self.client.get_or_create_collection(
                    name="talentscale_benchmarks",
                    metadata={"hnsw:space": "cosine"}
                )
                self._ingest_documents()
            except Exception as e:
                print(f"ChromaDB init warning: {e}. Using in-memory fallback.")
                self.available = False

    def _ingest_documents(self):
        """Ingest placeholder benchmark documents into ChromaDB."""
        if not self.collection:
            return

        existing = self.collection.count()
        if existing >= len(BENCHMARK_DOCUMENTS):
            return

        self.collection.upsert(
            ids=[d["id"] for d in BENCHMARK_DOCUMENTS],
            documents=[d["text"] for d in BENCHMARK_DOCUMENTS],
            metadatas=[d["metadata"] for d in BENCHMARK_DOCUMENTS],
        )

    def search(self, query: str, n_results: int = 3, company_type: str = None) -> List[str]:
        """Search for relevant benchmark documents."""
        if not self.available or not self.collection:
            return self._fallback_search(query)

        where = None
        if company_type:
            where = {"$or": [
                {"company_type": company_type},
                {"company_type": "all"}
            ]}

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(n_results, self.collection.count()),
                where=where,
            )
            return results["documents"][0] if results["documents"] else []
        except Exception:
            return self._fallback_search(query)

    def _fallback_search(self, query: str) -> List[str]:
        """Simple keyword-based fallback search."""
        query_lower = query.lower()
        scored = []
        for doc in BENCHMARK_DOCUMENTS:
            text = doc["text"].lower()
            score = sum(1 for word in query_lower.split() if word in text)
            if score > 0:
                scored.append((score, doc["text"]))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [text for _, text in scored[:3]]


# Singleton instance
_store: VectorStore = None


def get_vector_store() -> VectorStore:
    global _store
    if _store is None:
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        _store = VectorStore(persist_dir)
    return _store
