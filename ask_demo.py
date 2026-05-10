# ============================================================
#  ask_demo.py — Sunum için demo modu (API gerektirmez)
#  KULLANIM: python ask_demo.py
# ============================================================

import time

# ── Hazır sorular ve cevaplar ────────────────────────────────

DEMO_QA = [
    {
        "soru": "binary search nasıl çalışır",
        "kaynaklar": [
            ("algo_hafta3.pdf", 4, 0.921),
            ("algo_hafta3.pdf", 5, 0.887),
            ("veri_yapilari.pdf", 12, 0.843),
        ],
        "cevap": (
            "Binary search, sıralı bir dizi üzerinde çalışan verimli bir arama algoritmasıdır.\n\n"
            "Çalışma mantığı:\n"
            "  1. Dizinin ortasındaki elemana bak\n"
            "  2. Aranan değer ortadaki elemandan küçükse → sol yarıda devam et\n"
            "  3. Aranan değer ortadaki elemandan büyükse → sağ yarıda devam et\n"
            "  4. Eleman bulunana veya dizi bitene kadar tekrar et\n\n"
            "Zaman karmaşıklığı: O(log n)\n"
            "Önemli kısıt: Dizi sıralı olmalıdır, aksi halde çalışmaz.\n\n"
            "[Kaynak: algo_hafta3.pdf, Sayfa 4]"
        ),
    },
    {
        "soru": "midtermde hangi konular çıktı",
        "kaynaklar": [
            ("midterm_2024.pdf", 1, 0.912),
            ("midterm_2024.pdf", 2, 0.878),
            ("algo_hafta5.pdf",  1, 0.834),
        ],
        "cevap": (
            "2024 yılı midterm sınavında ağırlıklı olarak şu konulardan soru sorulmuştur:\n\n"
            "  • Sıralama algoritmaları (Quick Sort, Merge Sort) — 3 soru\n"
            "  • Özyineleme (Recursion) — 2 soru\n"
            "  • Binary Search — 1 soru\n"
            "  • Dinamik Programlamaya giriş — 1 soru\n\n"
            "Sınav formatı: 3 çoktan seçmeli + 2 açık uçlu soru\n"
            "Toplam süre: 90 dakika\n\n"
            "[Kaynak: midterm_2024.pdf, Sayfa 1]"
        ),
    },
    {
        "soru": "quick sort zaman karmaşıklığı",
        "kaynaklar": [
            ("algo_hafta5.pdf", 7, 0.934),
            ("algo_hafta5.pdf", 8, 0.901),
            ("veri_yapilari.pdf", 15, 0.856),
        ],
        "cevap": (
            "Quick Sort'un zaman karmaşıklığı duruma göre değişir:\n\n"
            "  • En iyi durum  : O(n log n) — pivot her seferinde ortayı seçer\n"
            "  • Ortalama durum: O(n log n) — pratikte genellikle bu\n"
            "  • En kötü durum : O(n²)      — pivot hep en büyük/küçük eleman\n\n"
            "En kötü durumu önlemek için:\n"
            "  → Rastgele pivot seçimi\n"
            "  → Median-of-three stratejisi\n\n"
            "Alan karmaşıklığı: O(log n) — özyinelemeli çağrı yığını\n\n"
            "[Kaynak: algo_hafta5.pdf, Sayfa 7]"
        ),
    },
    {
        "soru": "stack nedir",
        "kaynaklar": [
            ("veri_yapilari.pdf", 8, 0.945),
            ("veri_yapilari.pdf", 9, 0.912),
        ],
        "cevap": (
            "Stack (Yığın), LIFO (Last In First Out) prensibine göre çalışan bir veri yapısıdır.\n\n"
            "Temel operasyonlar:\n"
            "  • push(x) : Stack'e eleman ekle — O(1)\n"
            "  • pop()   : En üstteki elemanı çıkar — O(1)\n"
            "  • peek()  : En üstteki elemanı gör (çıkarmadan) — O(1)\n\n"
            "Kullanım alanları:\n"
            "  → Fonksiyon çağrı yığını (call stack)\n"
            "  → Parantez eşleştirme\n"
            "  → Geri alma (undo) işlemleri\n"
            "  → DFS (Derinlik Öncelikli Arama)\n\n"
            "[Kaynak: veri_yapilari.pdf, Sayfa 8]"
        ),
    },
    {
        "soru": "dynamic programming nedir",
        "kaynaklar": [
            ("dp_notlar.pdf", 3, 0.967),
            ("dp_notlar.pdf", 4, 0.923),
            ("algo_hafta7.pdf", 2, 0.887),
        ],
        "cevap": (
            "Dinamik Programlama (DP), büyük problemleri örtüşen alt problemlere bölen "
            "ve her alt problemi yalnızca bir kez çözen bir algoritma tasarım tekniğidir.\n\n"
            "İki temel özellik:\n"
            "  1. Optimal Alt Yapı: Problemin çözümü, alt problemlerin optimal çözümünden oluşur\n"
            "  2. Örtüşen Alt Problemler: Aynı alt problemler defalarca karşımıza çıkar\n\n"
            "İki yaklaşım:\n"
            "  • Top-Down (Memoization) : Özyineleme + önbellek\n"
            "  • Bottom-Up (Tabulation) : Tablo doldurma\n\n"
            "Klasik örnekler: Fibonacci, Knapsack, Longest Common Subsequence\n\n"
            "[Kaynak: dp_notlar.pdf, Sayfa 3]"
        ),
    },
    {
        "soru": "merge sort nasıl çalışır",
        "kaynaklar": [
            ("algo_hafta5.pdf", 3, 0.951),
            ("algo_hafta5.pdf", 4, 0.918),
        ],
        "cevap": (
            "Merge Sort, böl-ve-yönet (divide and conquer) stratejisine dayanan kararlı "
            "bir sıralama algoritmasıdır.\n\n"
            "Çalışma adımları:\n"
            "  1. Diziyi ikiye böl\n"
            "  2. Her iki yarıyı özyinelemeli olarak sırala\n"
            "  3. Sıralanmış iki yarıyı birleştir (merge)\n\n"
            "Karmaşıklık:\n"
            "  • Zaman: O(n log n) — her durumda (en iyi, ortalama, en kötü)\n"
            "  • Alan : O(n) — birleştirme için ekstra dizi gerekir\n\n"
            "Quick Sort'tan farkı: Kararlıdır (stable) ve her durumda O(n log n) garantisi verir.\n\n"
            "[Kaynak: algo_hafta5.pdf, Sayfa 3]"
        ),
    },
]


# ── Yardımcı fonksiyonlar ────────────────────────────────────

def find_answer(query: str):
    """Sorguya en yakın demo cevabı bulur."""
    query_lower = query.lower().strip()
    for qa in DEMO_QA:
        # Anahtar kelimeleri kontrol et
        keywords = qa["soru"].split()
        matches  = sum(1 for kw in keywords if kw in query_lower)
        if matches >= 1:
            return qa
    return None


def print_result(query: str, qa: dict):
    """Sonucu sunum formatında yazdırır."""
    print(f"\n{'='*57}")
    print(f"  Sorgu : {query}")
    print(f"{'='*57}")

    print(f"\n  [1/3] Embedding alınıyor...")
    time.sleep(0.6)

    print(f"  [2/3] {len(qa['kaynaklar'])} kaynak bulundu:")
    time.sleep(0.4)
    for kaynak, sayfa, skor in qa["kaynaklar"]:
        time.sleep(0.2)
        print(f"        → {kaynak} s.{sayfa}  (skor: {skor:.3f})")

    print(f"  [3/3] GPT-4o cevap üretiyor...")
    time.sleep(1.0)

    print(f"\n  Cevap:")
    print(f"  {'-'*50}")
    for satir in qa["cevap"].split("\n"):
        print(f"  {satir}")
        time.sleep(0.05)
    print(f"  {'-'*50}")
    print(f"{'='*57}\n")


def print_not_found(query: str):
    """Bulunamayan sorgu mesajı."""
    print(f"\n{'='*57}")
    print(f"  Sorgu : {query}")
    print(f"{'='*57}")
    print(f"\n  [1/3] Embedding alınıyor...")
    time.sleep(0.5)
    print(f"  [2/3] Arama yapılıyor...")
    time.sleep(0.5)
    print(f"  [3/3] Sonuç değerlendiriliyor...")
    time.sleep(0.5)
    print(f"\n  Cevap:")
    print(f"  {'-'*50}")
    print(f"  Bu bilgi ders materyallerinde bulunamadı.")
    print(f"  Yüklü PDF'ler bu konuyu kapsamamaktadır.")
    print(f"  {'-'*50}")
    print(f"{'='*57}\n")


def print_welcome():
    print("\n" + "="*57)
    print("  🎓 ÜNİVERSİTE DERS ASİSTANI — Demo Modu")
    print("  RAG Tabanlı Akıllı Soru-Cevap Sistemi")
    print("  Geliştiren: Miraç KESKİN")
    print("="*57)
    print("\n  📂 Yüklü PDF'ler:")
    pdf_list = [
        "algo_hafta3.pdf   → Binary Search, Arama Algoritmaları",
        "algo_hafta5.pdf   → Sorting Algoritmaları (Quick/Merge Sort)",
        "algo_hafta7.pdf   → Dinamik Programlama",
        "midterm_2024.pdf  → Geçmiş Sınav Soruları",
        "veri_yapilari.pdf → Stack, Queue, Linked List",
        "dp_notlar.pdf     → DP Notları ve Örnekler",
    ]
    for pdf in pdf_list:
        print(f"    • {pdf}")

    print("\n  💡 Örnek sorular:")
    ornek = [
        "Binary search nasıl çalışır?",
        "Midtermde hangi konular çıktı?",
        "Quick sort zaman karmaşıklığı nedir?",
        "Stack nedir?",
        "Dynamic programming nedir?",
        "Merge sort nasıl çalışır?",
    ]
    for s in ornek:
        print(f"    → {s}")

    print("\n  Çıkmak için: q\n")


# ── Ana döngü ────────────────────────────────────────────────

def main():
    print_welcome()

    while True:
        try:
            query = input("❓ Sorunuz: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGüle güle!")
            break

        if not query:
            continue
        if query.lower() in ("q", "exit", "quit", "çıkış"):
            print("Güle güle!")
            break

        qa = find_answer(query)
        if qa:
            print_result(query, qa)
        else:
            print_not_found(query)


if __name__ == "__main__":
    main()
