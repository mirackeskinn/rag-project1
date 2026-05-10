# ============================================================
#  chunker.py — Metinleri 300-token pencerelerle böler
# ============================================================

from dataclasses import dataclass, field
from typing import List

import tiktoken

from parser import ParsedPage


@dataclass
class Chunk:
    chunk_id:    int
    source_file: str
    page_number: int
    heading:     str
    text:        str
    token_count: int
    entities:    List[dict] = field(default_factory=list)
    embedding:   List[float] = field(default_factory=list)


# ── Encoding ─────────────────────────────────────────────────

_enc = tiktoken.get_encoding("cl100k_base")

def _tokenize(text: str) -> List[int]:
    return _enc.encode(text)

def _detokenize(tokens: List[int]) -> str:
    return _enc.decode(tokens)


# ── Sliding-window chunking ───────────────────────────────────

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """Metni token bazlı, örtüşmeli parçalara böler."""
    tokens = _tokenize(text)
    chunks = []
    start  = 0

    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(_detokenize(tokens[start:end]))
        if end == len(tokens):
            break
        start += chunk_size - overlap

    return chunks


def create_chunks(pages: List[ParsedPage],
                  chunk_size: int = 300,
                  overlap: int    = 50) -> List[Chunk]:
    """Tüm sayfaları başlık-farkında chunk'lara dönüştürür."""
    all_chunks = []
    chunk_id   = 0

    for page in pages:
        # Başlık her chunk'ın önüne eklenerek bağlam zenginleştirilir
        enriched = f"[{page.heading}] {page.text}"
        parts    = chunk_text(enriched, chunk_size, overlap)

        for part in parts:
            all_chunks.append(Chunk(
                chunk_id=chunk_id,
                source_file=page.source_file,
                page_number=page.page_number,
                heading=page.heading,
                text=part,
                token_count=len(_tokenize(part)),
            ))
            chunk_id += 1

    return all_chunks
