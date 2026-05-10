# 🎓 Üniversite Ders Asistanı — RAG Sistemi

**Miraç KESKİN** | GitHub: https://github.com/mirackeskinn/rag-project1

PDF ders notlarından anlam tabanlı soru-cevap sistemi.
OpenAI GPT-4o + text-embedding-3-small + FAISS + spaCy

---

## 📁 Proje Yapısı

```
university_rag/
├── config.py          ← API key ve tüm ayarlar BURADAN yapılır
├── parser.py          ← PDF → metin (PyMuPDF)
├── chunker.py         ← Metin → 300-token chunk'lar
├── ner.py             ← spaCy varlık tanıma
├── embedder.py        ← OpenAI embedding
├── vector_store.py    ← FAISS indeks (kaydet/yükle/ara)
├── rag.py             ← Retrieval + Generation pipeline
├── index_pdfs.py      ← [1. ADIM] PDF'leri indeksle
├── ask.py             ← [2. ADIM] Soru sor
├── requirements.txt
├── pdfs/              ← PDF dosyalarınızı buraya atın
└── tests/
    └── test_modules.py ← Her modülü bağımsız test et
```

---

## 🚀 Kurulum ve Çalıştırma (Adım Adım)

### 1. Paketleri kur
```bash
pip install -r requirements.txt
python -m spacy download tr_core_news_sm
```

### 2. API key'i ayarla
`config.py` dosyasını aç ve şu satırı düzenle:
```python
"openai_api_key": "sk-..."   # kendi anahtarını yaz
```

### 3. PDF'leri ekle
Ders PDF'lerini `pdfs/` klasörüne kopyala.

### 4. Testleri çalıştır (her şey kuruldu mu?)
```bash
python tests/test_modules.py
```
Tüm satırlarda ✅ görünüyorsa devam et.

### 5. PDF'leri indeksle (bir kez çalıştır)
```bash
python index_pdfs.py
```
Bu adım: parse → chunk → NER → embed → FAISS kaydet

### 6. Soru sor!
```bash
python ask.py
```
```
❓ Sorunuz: Binary search nasıl çalışır?
```

---

## 🔧 Sorun Giderme

| Hata | Çözüm |
|------|-------|
| `ModuleNotFoundError: fitz` | `pip install pymupdf` |
| `ModuleNotFoundError: faiss` | `pip install faiss-cpu` |
| `OSError: model not found` | `python -m spacy download tr_core_news_sm` |
| `AuthenticationError` | config.py'deki API key'i kontrol et |
| `No PDF found` | pdfs/ klasörüne PDF ekle |
| `Index not found` | Önce `python index_pdfs.py` çalıştır |

---

## 💡 Sistem Akışı

```
[index_pdfs.py]
PDF'ler → parse → chunk (300t/50 overlap) → NER → embed → FAISS kaydet

[ask.py]
Soru → embed → FAISS ara (top-5) → GPT-4o → Türkçe cevap
```
