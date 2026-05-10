# ============================================================
#  rag.py — Retrieval + Generation: tam RAG pipeline
# ============================================================

from typing import List, Dict

import faiss
import numpy as np
from openai import OpenAI

from vector_store import search


# ── Sistem Promptu ────────────────────────────────────────────

SYSTEM_PROMPT = """Sen bir üniversite ders asistanısın.
Sana verilen bağlam bilgisine (ders notları ve slaytlardan alınan parçalar) dayanarak
öğrencilerin sorularını Türkçe olarak yanıtla.

Kurallar:
1. Yalnızca verilen bağlamdaki bilgileri kullan.
2. Bağlamda yoksa: "Bu bilgi ders materyallerinde bulunamadı." de.
3. Her cevabın sonunda kaynağı belirt: [Kaynak: dosya_adı, Sayfa X]
4. Kısa, net ve öğrenci dostu bir dil kullan.
5. Teknik terimleri Türkçe açıkla."""


# ── Retrieval ─────────────────────────────────────────────────

def get_query_embedding(
    client: OpenAI,
    query:  str,
    model:  str = "text-embedding-3-small",
) -> np.ndarray:
    """Sorgu metnini normalize edilmiş embedding vektörüne çevirir."""
    response  = client.embeddings.create(input=[query], model=model)
    vec       = np.array([response.data[0].embedding], dtype=np.float32)
    faiss.normalize_L2(vec)
    return vec


def retrieve(
    client:   OpenAI,
    query:    str,
    index:    faiss.Index,
    metadata: List[Dict],
    top_k:    int = 5,
    emb_model: str = "text-embedding-3-small",
) -> List[Dict]:
    """Sorguya en benzer top_k chunk'ı getirir."""
    vec = get_query_embedding(client, query, model=emb_model)
    return search(vec, index, metadata, top_k=top_k)


# ── Generation ────────────────────────────────────────────────

def _format_context(chunks: List[Dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(
            f"[Kaynak {i}: {c['source_file']}, Sayfa {c['page_number']}]\n{c['text']}"
        )
    return "\n\n".join(parts)


def generate(
    client:  OpenAI,
    query:   str,
    chunks:  List[Dict],
    model:   str = "gpt-4o",
) -> str:
    """Getirilen chunk'lara dayanarak GPT-4o ile cevap üretir."""
    context      = _format_context(chunks)
    user_message = f"Bağlam:\n{context}\n\n---\nSoru: {query}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.2,
        max_tokens=800,
    )
    return response.choices[0].message.content


# ── Tam Pipeline ─────────────────────────────────────────────

def rag_query(
    client:    OpenAI,
    query:     str,
    index:     faiss.Index,
    metadata:  List[Dict],
    top_k:     int  = 5,
    emb_model: str  = "text-embedding-3-small",
    llm_model: str  = "gpt-4o",
    verbose:   bool = True,
) -> str:
    """
    Uçtan uca RAG:
      1. Sorgu → embedding
      2. FAISS similarity search
      3. GPT-4o ile cevap üretimi
    """
    if verbose:
        print(f"\n{'='*55}")
        print(f"  Sorgu : {query}")
        print(f"{'='*55}")
        print("  [1/3] Embedding alınıyor...")

    retrieved = retrieve(client, query, index, metadata, top_k, emb_model)

    if verbose:
        print(f"  [2/3] {len(retrieved)} kaynak bulundu:")
        for r in retrieved:
            print(f"        → {r['source_file']} s.{r['page_number']}"
                  f"  (skor: {r['similarity_score']:.3f})")
        print("  [3/3] GPT-4o cevap üretiyor...")

    answer = generate(client, query, retrieved, model=llm_model)

    if verbose:
        print(f"\n  Cevap:\n{answer}")
        print(f"{'='*55}\n")

    return answer
