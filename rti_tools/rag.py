"""
rti_tools/rag.py — RAG retrieval over the RTI Act knowledge base.
Uses sentence-transformers for local embeddings + FAISS for similarity search.
No external API calls required for retrieval.
"""

from __future__ import annotations

import numpy as np
from typing import List, Tuple

from knowledge_base.rti_act_provisions import RTI_ACT_CHUNKS

# ─── lazy-load sentence-transformers so Flask starts fast ──────────────────
_model = None
_index = None
_chunk_texts: List[str] = []
_chunk_meta: List[dict] = []


def _ensure_index() -> None:
    """Build the FAISS index lazily on first retrieval call."""
    global _model, _index, _chunk_texts, _chunk_meta

    if _index is not None:
        return  # already built

    import faiss
    from sentence_transformers import SentenceTransformer

    _model = SentenceTransformer("all-MiniLM-L6-v2")  # ~80 MB, fast CPU model

    _chunk_texts = [f"{c['title']}\n\n{c['text']}" for c in RTI_ACT_CHUNKS]
    _chunk_meta = RTI_ACT_CHUNKS

    embeddings = _model.encode(_chunk_texts, convert_to_numpy=True, normalize_embeddings=True)
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)  # inner-product on normalized vectors = cosine similarity
    _index.add(embeddings.astype("float32"))


def retrieve(query: str, k: int = 4) -> List[dict]:
    """
    Retrieve the top-k most relevant RTI Act chunks for the given query.
    Returns a list of dicts with keys: id, title, text, tags, score.
    """
    _ensure_index()

    query_vec = _model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    scores, indices = _index.search(query_vec.astype("float32"), k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        chunk = dict(_chunk_meta[idx])
        chunk["score"] = float(score)
        results.append(chunk)
    return results


def format_context(chunks: List[dict]) -> str:
    """Format retrieved chunks into a single context string for the LLM prompt."""
    if not chunks:
        return "No relevant provisions found."
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[Source {i}: {c['title']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)
