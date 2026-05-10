# ============================================================
#  ner.py — spaCy ile varlık tanıma (NER)
# ============================================================

from typing import List, Dict
import spacy
from spacy.pipeline import EntityRuler

from chunker import Chunk


def load_nlp(model_name: str = "tr_core_news_sm"):
    """spaCy modelini yükler ve özel akademik kalıpları ekler."""
    try:
        nlp = spacy.load(model_name)
    except OSError:
        raise OSError(
            f"spaCy modeli '{model_name}' bulunamadı.\n"
            f"Çözüm: python -m spacy download {model_name}"
        )

    # Özel kural tabanlı etiketler (akademik terimler)
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        # Algoritmalar / Konular
        {"label": "TOPIC", "pattern": "binary search"},
        {"label": "TOPIC", "pattern": "sorting"},
        {"label": "TOPIC", "pattern": "recursion"},
        {"label": "TOPIC", "pattern": "dynamic programming"},
        {"label": "TOPIC", "pattern": "quick sort"},
        {"label": "TOPIC", "pattern": "merge sort"},
        {"label": "TOPIC", "pattern": "stack"},
        {"label": "TOPIC", "pattern": "queue"},
        {"label": "TOPIC", "pattern": "linked list"},
        {"label": "TOPIC", "pattern": "makine öğrenmesi"},
        {"label": "TOPIC", "pattern": "yapay zeka"},
        # Sınav türleri
        {"label": "EXAM", "pattern": [{"LOWER": {"IN": ["midterm", "vize", "final", "quiz"]}}]},
    ]
    ruler.add_patterns(patterns)
    return nlp


def extract_entities(nlp, text: str) -> List[Dict]:
    """Metinden NER varlıklarını çıkarır."""
    doc  = nlp(text[:1000])   # performans için ilk 1000 karakter
    seen = set()
    entities = []
    for ent in doc.ents:
        key = (ent.text.lower(), ent.label_)
        if key not in seen:
            entities.append({"text": ent.text, "label": ent.label_})
            seen.add(key)
    return entities


def apply_ner(nlp, chunks: List[Chunk]) -> List[Chunk]:
    """Tüm chunk'lara NER uygular."""
    print("[+] NER uygulanıyor...")
    for i, chunk in enumerate(chunks):
        chunk.entities = extract_entities(nlp, chunk.text)
        if (i + 1) % 200 == 0:
            print(f"    {i+1}/{len(chunks)} chunk işlendi")
    print(f"[+] NER tamamlandı.\n")
    return chunks
