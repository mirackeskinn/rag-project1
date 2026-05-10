# ============================================================
#  parser.py — PDF dosyalarını metin + başlık olarak çıkarır
# ============================================================

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

import fitz  # PyMuPDF


@dataclass
class ParsedPage:
    source_file: str
    page_number: int
    heading: str
    text: str


# ── Yardımcı fonksiyonlar ────────────────────────────────────

def clean_text(text: str) -> str:
    """Ham PDF metnini temizler."""
    text = re.sub(r"([a-z])-\n([a-z])", r"\1\2", text)   # tire satır kırma
    text = re.sub(r"\n+", " ", text)                       # satır sonlarını boşluğa çevir
    text = re.sub(r"\s{2,}", " ", text)                    # çoklu boşluk
    return text.strip()


def extract_heading(page: fitz.Page) -> str:
    """Sayfadaki en büyük font boyutlu metni başlık olarak döndürür."""
    candidates = []
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if span["size"] >= 14 and len(span["text"].strip()) > 3:
                    candidates.append((span["size"], span["text"].strip()))

    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1][:100]
    return "Başlık Yok"


# ── Ana fonksiyonlar ─────────────────────────────────────────

def parse_pdf(pdf_path: str) -> List[ParsedPage]:
    """Tek bir PDF dosyasını sayfa sayfa parse eder."""
    pages = []
    doc = fitz.open(pdf_path)
    file_name = Path(pdf_path).name

    for page_num in range(len(doc)):
        page = doc[page_num]
        raw  = page.get_text("text")
        text = clean_text(raw)
        if len(text) < 50:          # boş/çok kısa sayfaları atla
            continue
        pages.append(ParsedPage(
            source_file=file_name,
            page_number=page_num + 1,
            heading=extract_heading(page),
            text=text,
        ))

    doc.close()
    return pages


def parse_all_pdfs(pdf_dir: str) -> List[ParsedPage]:
    """Klasördeki tüm PDF'leri parse eder."""
    all_pages = []
    pdf_files = list(Path(pdf_dir).glob("*.pdf"))

    if not pdf_files:
        print(f"[!] '{pdf_dir}' klasöründe PDF bulunamadı.")
        print("    Lütfen PDF dosyalarınızı bu klasöre kopyalayın.")
        return []

    print(f"[+] {len(pdf_files)} PDF bulundu.")
    for path in pdf_files:
        try:
            pages = parse_pdf(str(path))
            all_pages.extend(pages)
            print(f"    ✓ {path.name} → {len(pages)} sayfa")
        except Exception as e:
            print(f"    ✗ {path.name} HATA: {e}")

    print(f"[+] Toplam {len(all_pages)} sayfa parse edildi.\n")
    return all_pages
