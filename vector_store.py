# ============================================================
#  vector_store.py — FAISS indeks: oluştur / kaydet / yükle / ara
# ============================================================

import json
from typing import List, Dict, Tuple

import faiss
import numpy as np

from chunker import Chunk


# ── İndeks oluşturma ─────────────────────────────────────────

def build_index(chunks: List[Chunk]) -> faiss.Index:
    """Chunk embedding'lerinden FAISS cosine-similarity indeksi oluşturur."""
    vectors = np.array([c.embedding for c in chunks], dtype=np.float32)
    faiss.normalize_L2(vectors)                    # cosine similarity için normalize et

    dim   = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)                 # Inner Product == cosine (normalize sonrası)
    index.add(vectors)

    print(f"[+] FAISS indeksi oluşturuldu: {index.ntotal} vektör, {dim}D\n")
    return index


# ── Kaydet / Yükle ───────────────────────────────────────────

def save(index: faiss.Index, chunks: List[Chunk],
         index_path: str, metadata_path: str) -> None:
    """İndeksi ve chunk metadata'sını diske yazar."""
    faiss.write_index(index, index_path)

    metadata = [
        {
            "chunk_id":    c.chunk_id,
            "source_file": c.source_file,
            "page_number": c.page_number,
            "heading":     c.heading,
            "text":        c.text,
            "token_count": c.token_count,
            "entities":    c.entities,
        }
        for c in chunks
    ]
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"[+] İndeks kaydedildi   → {index_path}")
    print(f"[+] Metadata kaydedildi → {metadata_path}\n")


def load(index_path: str, metadata_path: str) -> Tuple[faiss.Index, List[Dict]]:
    """Kaydedilmiş indeks ve metadata'yı yükler."""
    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    print(f"[+] İndeks yüklendi: {index.ntotal} vektör\n")
    return index, metadata


# ── Arama ────────────────────────────────────────────────────

def search(
    query_vec: np.ndarray,
    index:     faiss.Index,
    metadata:  List[Dict],
    top_k:     int = 5,
) -> List[Dict]:
    """Sorgu vektörüne en yakın top_k chunk'ı döndürür."""
    scores, indices = index.search(query_vec, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if 0 <= idx < len(metadata):
            item = dict(metadata[idx])
            item["similarity_score"] = float(score)
            results.append(item)
    return results
