# ============================================================
#  tests/test_modules.py — Her modülü bağımsız olarak test eder
#  KULLANIM: python tests/test_modules.py
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np


def separator(title):
    print(f"\n{'─'*50}")
    print(f"  TEST: {title}")
    print(f"{'─'*50}")


# ── TEST 1: Import kontrolü ───────────────────────────────────
separator("Import Kontrolü")
try:
    import fitz
    print("  ✅ PyMuPDF (fitz)")
except ImportError:
    print("  ❌ PyMuPDF eksik → pip install pymupdf")

try:
    import tiktoken
    print("  ✅ tiktoken")
except ImportError:
    print("  ❌ tiktoken eksik → pip install tiktoken")

try:
    import spacy
    print("  ✅ spaCy")
except ImportError:
    print("  ❌ spaCy eksik → pip install spacy")

try:
    import faiss
    print("  ✅ FAISS")
except ImportError:
    print("  ❌ FAISS eksik → pip install faiss-cpu")

try:
    import openai
    print("  ✅ openai")
except ImportError:
    print("  ❌ openai eksik → pip install openai")


# ── TEST 2: Config ────────────────────────────────────────────
separator("Config")
from config import CONFIG
print(f"  Embedding model : {CONFIG['embedding_model']}")
print(f"  LLM model       : {CONFIG['llm_model']}")
print(f"  Chunk size      : {CONFIG['chunk_size']} token")
print(f"  Chunk overlap   : {CONFIG['chunk_overlap']} token")
print(f"  Top-k           : {CONFIG['top_k']}")
api_key = CONFIG["openai_api_key"]
if api_key.startswith("sk-") and len(api_key) > 10:
    print(f"  API key         : ✅ Ayarlanmış ({api_key[:8]}...)")
else:
    print(f"  API key         : ❌ config.py içinde ayarlanmamış!")


# ── TEST 3: Chunker (API gerektirmez) ─────────────────────────
separator("Chunker — Token Tabanlı Bölme")
from chunker import chunk_text, _tokenize

sample_text = (
    "Binary search, sıralı bir dizi üzerinde O(log n) karmaşıklığıyla çalışan "
    "bir arama algoritmasıdır. Her adımda dizi ortadan ikiye bölünür. "
    "Aranan değer ortadaki elemandan küçükse sol yarı, büyükse sağ yarı seçilir. "
    "Bu işlem eleman bulunana veya dizi bitene kadar devam eder. "
    "Yöntem, doğrusal aramaya (O(n)) kıyasla büyük veri setlerinde çok daha hızlıdır."
)

chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
print(f"  Giriş metni  : {len(_tokenize(sample_text))} token")
print(f"  Chunk sayısı : {len(chunks)}")
for i, c in enumerate(chunks):
    print(f"  Chunk {i+1}      : {len(_tokenize(c))} token — '{c[:60]}...'")
print("  ✅ Chunker çalışıyor")


# ── TEST 4: spaCy NER (model indirilmişse) ────────────────────
separator("spaCy NER")
try:
    from ner import load_nlp, extract_entities
    nlp      = load_nlp(CONFIG["spacy_model"])
    test_txt = "Binary search algoritması midterm sınavında soruldu."
    ents     = extract_entities(nlp, test_txt)
    print(f"  Metin      : '{test_txt}'")
    print(f"  Bulunanlar : {ents}")
    print("  ✅ spaCy NER çalışıyor")
except OSError as e:
    print(f"  ⚠️  {e}")
except Exception as e:
    print(f"  ❌ Beklenmedik hata: {e}")


# ── TEST 5: FAISS (API gerektirmez) ──────────────────────────
separator("FAISS — Vektör Araması")
import faiss as _faiss

dim       = 8
n_vectors = 5
vectors   = np.random.rand(n_vectors, dim).astype(np.float32)
_faiss.normalize_L2(vectors)

index = _faiss.IndexFlatIP(dim)
index.add(vectors)

query = np.random.rand(1, dim).astype(np.float32)
_faiss.normalize_L2(query)
scores, indices = index.search(query, 3)

print(f"  {n_vectors} vektör ({dim}D) indekslendi")
print(f"  Top-3 sonuç: indeksler={indices[0].tolist()}, skorlar={[f'{s:.3f}' for s in scores[0]]}")
print("  ✅ FAISS çalışıyor")


# ── TEST 6: OpenAI API bağlantısı ─────────────────────────────
separator("OpenAI API Bağlantısı")
if not CONFIG["openai_api_key"].startswith("sk-") or len(CONFIG["openai_api_key"]) < 20:
    print("  ⚠️  API key ayarlanmamış — bu test atlandı.")
    print("      config.py içindeki openai_api_key değerini güncelleyin.")
else:
    try:
        from openai import OpenAI
        client   = OpenAI(api_key=CONFIG["openai_api_key"])
        response = client.embeddings.create(
            input=["test"],
            model=CONFIG["embedding_model"],
        )
        dim = len(response.data[0].embedding)
        print(f"  Embedding boyutu : {dim}D")
        print("  ✅ OpenAI API bağlantısı başarılı")
    except Exception as e:
        print(f"  ❌ OpenAI API hatası: {e}")


# ── Özet ──────────────────────────────────────────────────────
print("\n" + "="*50)
print("  Tüm testler tamamlandı.")
print("  ❌ varsa o modülü pip install ile kurun.")
print("  Sonra: python index_pdfs.py → python ask.py")
print("="*50 + "\n")
