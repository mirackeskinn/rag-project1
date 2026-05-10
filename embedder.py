# ============================================================
#  embedder.py — OpenAI text-embedding-3-small ile vektör üretimi
# ============================================================

import time
from typing import List

import numpy as np
from openai import OpenAI

from chunker import Chunk


def get_embeddings_batch(
    client:     OpenAI,
    texts:      List[str],
    model:      str = "text-embedding-3-small",
    batch_size: int = 100,
) -> List[List[float]]:
    """Metinleri batch halinde embed eder."""
    all_embeddings = []
    total_batches  = (len(texts) + batch_size - 1) // batch_size

    for i in range(0, len(texts), batch_size):
        batch     = texts[i : i + batch_size]
        batch_num = i // batch_size + 1
        try:
            response = client.embeddings.create(input=batch, model=model)
            all_embeddings.extend(item.embedding for item in response.data)
            print(f"    Batch {batch_num}/{total_batches} ✓  ({len(batch)} metin)")
            time.sleep(0.3)                         # rate-limit koruması
        except Exception as e:
            print(f"    Batch {batch_num} HATA: {e}")
            all_embeddings.extend([[0.0] * 1536] * len(batch))   # hata yedeği

    return all_embeddings


def embed_chunks(
    client: OpenAI,
    chunks: List[Chunk],
    model:  str = "text-embedding-3-small",
) -> List[Chunk]:
    """Tüm chunk'ları embed eder ve sonuçları chunk nesnelerine yazar."""
    print(f"[+] {len(chunks)} chunk embed ediliyor...")
    texts      = [c.text for c in chunks]
    embeddings = get_embeddings_batch(client, texts, model=model)

    for chunk, emb in zip(chunks, embeddings):
        chunk.embedding = emb

    dim = len(embeddings[0]) if embeddings else 0
    print(f"[+] Embedding tamamlandı. Boyut: {dim}D\n")
    return chunks
