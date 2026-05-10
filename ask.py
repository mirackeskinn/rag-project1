# ============================================================
#  ask.py — İnteraktif soru-cevap terminali
#  KULLANIM: python ask.py
#  ÖNKOŞUl: index_pdfs.py daha önce çalıştırılmış olmalı
# ============================================================

from pathlib import Path
from openai import OpenAI

from config       import CONFIG
from vector_store import load
from rag          import rag_query


def main():
    # İndeks dosyalarını kontrol et
    if not Path(CONFIG["index_path"]).exists():
        print("\n[!] FAISS indeksi bulunamadı.")
        print("    Önce şunu çalıştırın: python index_pdfs.py\n")
        return

    print("\n" + "="*55)
    print("  ÜNİVERSİTE DERS ASİSTANI — Soru-Cevap Modu")
    print("  Çıkmak için: 'q' veya 'exit' yazın")
    print("="*55 + "\n")

    # İstemci ve indeksi yükle
    client          = OpenAI(api_key=CONFIG["openai_api_key"])
    index, metadata = load(CONFIG["index_path"], CONFIG["metadata_path"])

    # Soru-cevap döngüsü
    while True:
        try:
            query = input("❓ Sorunuz: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGüle güle!")
            break

        if not query:
            continue
        if query.lower() in ("q", "exit", "çıkış", "quit"):
            print("Güle güle!")
            break

        rag_query(
            client=client,
            query=query,
            index=index,
            metadata=metadata,
            top_k=CONFIG["top_k"],
            emb_model=CONFIG["embedding_model"],
            llm_model=CONFIG["llm_model"],
            verbose=True,
        )


if __name__ == "__main__":
    main()
