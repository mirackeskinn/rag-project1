# ============================================================
#  config.py — Tüm sistem ayarları tek yerden yönetilir
# ============================================================

CONFIG = {
    # --- OpenAI ---
    "openai_api_key":   "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",           # <-- KENDİ ANAHTARINIZI GİRİN
    "embedding_model":  "text-embedding-3-small",
    "llm_model":        "gpt-4o",

    # --- Chunking ---
    "chunk_size":       300,                # token
    "chunk_overlap":    50,                 # token

    # --- Retrieval ---
    "top_k":            5,                  # kaç chunk getirilsin

    # --- Dosya Yolları ---
    "pdf_dir":          "./pdfs",           # PDF'lerinizi buraya atın
    "index_path":       "./faiss_index.bin",
    "metadata_path":    "./chunks_metadata.json",

    # --- spaCy ---
    "spacy_model":      "en_core_web_sm",  # Türkçe; İngilizce: en_core_web_sm
}
