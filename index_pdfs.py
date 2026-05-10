# ============================================================
#  index_pdfs.py — PDF'leri işle ve FAISS indeksini oluştur
#  KULLANIM: python index_pdfs.py
#  NOT: Bu script bir kez çalıştırılır. Sonraki sorgular için
#       faiss_index.bin ve chunks_metadata.json kullanılır.
# ============================================================

import numpy as np
from openai import OpenAI

from config        import CONFIG
from parser        import parse_all_pdfs
from chunker       import create_chunks
from ner           import load_nlp, apply_ner
from embedder      import embed_chunks
from vector_store  import build_index, save


def main():
    print("\n" + "="*55)
    print("  ÜNİVERSİTE DERS ASİSTANI — İndeksleme Başlıyor")
    print("="*55 + "\n")

    # 0. OpenAI istemcisi
    client = OpenAI(api_key=CONFIG["openai_api_key"])

    # 1. PDF Parsing
    print("[ADIM 1] PDF'ler parse ediliyor...")
    pages = parse_all_pdfs(CONFIG["pdf_dir"])
    if not pages:
        print("[!] Hiç sayfa bulunamadı. Çıkılıyor.")
        return

    # 2. Chunking
    print("[ADIM 2] Chunk'lara bölünüyor...")
    chunks = create_chunks(pages, CONFIG["chunk_size"], CONFIG["chunk_overlap"])
    print(f"[+] {len(chunks)} chunk oluşturuldu.\n")

    # İstatistik
    token_counts = [c.token_count for c in chunks]
    print(f"    Ortalama token/chunk : {np.mean(token_counts):.0f}")
    print(f"    Min / Max            : {min(token_counts)} / {max(token_counts)}\n")

    # 3. NER
    print("[ADIM 3] NER uygulanıyor...")
    nlp    = load_nlp(CONFIG["spacy_model"])
    chunks = apply_ner(nlp, chunks)

    # 4. Embedding
    print("[ADIM 4] Embedding üretiliyor...")
    chunks = embed_chunks(client, chunks, model=CONFIG["embedding_model"])

    # 5. FAISS indeks oluştur ve kaydet
    print("[ADIM 5] FAISS indeksi oluşturuluyor...")
    index = build_index(chunks)
    save(index, chunks, CONFIG["index_path"], CONFIG["metadata_path"])

    print("\n" + "="*55)
    print("  İndeksleme tamamlandı!")
    print(f"  Toplam chunk : {len(chunks)}")
    print(f"  İndeks       : {CONFIG['index_path']}")
    print(f"  Metadata     : {CONFIG['metadata_path']}")
    print("  Şimdi 'python ask.py' ile sorgu yapabilirsiniz.")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()
