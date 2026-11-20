# Draf Rancangan Pengerjaan Tugas Tree-sitter (Tugas 1–6)

* **Nama:** Kemal Melvin Ibrahim
* **NIM / Kelas:** 017 / 2A
* **Mata Kuliah:** Programming Language Pragmatics (PLP)

---

## 1. Tujuan & Latar Belakang
Mempelajari cara kerja *Concrete Syntax Tree* (CST) dan *pattern matching* berbasis Tree-sitter, lalu menerapkannya untuk membangun dua perangkat nyata pendukung pengembangan perangkat lunak:
1. **DSL Filter Enterprise (`tree-sitter-filter`)**: bahasa kueri pencarian admin beserta *syntax highlighting* dan konverter ke SQL `WHERE` berparameter (`?`).
2. **CLI Analisis Statis (`cek.py`)**: pemeriksa otomatis komentar `TODO`/`FIXME`, fungsi panjang (`> 30` baris), dan *syntax error* pada basis kode Python dan JavaScript.

---

## 2. Rancangan Arsitektur & Komponen

| Modul / Folder | Tugas | Rancangan & Fungsi Utama |
| :--- | :---: | :--- |
| **`tugas1-3/`** | 1–3 | Eksplorasi CST (`t1.py`), traversal rekursif & `TreeCursor` (`jelajah.py`), serta penjalan query deklaratif (`q.py`) dengan berkas `.scm` (`semua.scm`, `fungsi.scm`, `print.scm`, `import.scm`, `docstring.scm`). |
| **`tree-sitter-filter/`** | 4–5 | Grammar DSL `filter` di `grammar.js` (`comparison`, `and`/`or`/`not`, `parenthesized`, `in_expression`, `contains`), *corpus test* di `test/corpus/dasar.txt`, `queries/highlights.scm`, dan pengayaan `filter_to_sql.py`. |
| **`cek/`** | 6 | CLI multi-bahasa `cek.py <folder>` berbasis pemetaan `KONFIG_BAHASA` (`.py` dan `.js`), melewati `.venv`/`.git`/`node_modules`, lengkap dengan skenario uji `cek/uji/` dan `README.md`. |

---

## 3. Rancangan Query Inti & Alasan Memilih Tree-sitter

Contoh pola S-expression utama yang dirancang di proyek ini:

```scheme
;; Menangkap komentar TODO/FIXME tanpa salah mendeteksi teks di dalam string
((comment) @c (#match? @c "TODO|FIXME"))

;; Menangkap fungsi beserta jumlah barisnya melalui koordinat node
(function_definition name: (identifier) @nama) @fungsi
```

* **Dibanding Regex:** Pencocokan berbasis pohon memastikan kata kunci di dalam string literal (misal `"TODO: ..."` atau `"open and pending"`) tetap dikenali sebagai `string`, bukan komentar atau operator.
* **Dibanding Pengecekan AI per Berkas:** Eksekusi lokal bersifat deterministik (hasil selalu konsisten), tanpa biaya token, dan cepat memindai banyak berkas sekaligus.

---

## 4. Rencana Pengujian & Evaluasi

1. **Verifikasi Traversal & Query (Tugas 1–3):** Membandingkan output rekursif vs `TreeCursor` pada `analyzer.py` (102 baris) dengan mode `--cek`, serta mencocokkan hasil query terhadap hitungan manual.
2. **Corpus & Highlight Check (Tugas 4–5):** Menjalankan `tree-sitter test` (minimal 5 kasus uji meliputi prioritas `and`/`or`, kurung, `not`, `string`/`number`/`boolean`, `in`, dan `contains`) dan `tree-sitter highlight --check`.
3. **Uji Repositori Nyata (Tugas 6):** Menjalankan `cek.py` pada folder uji lokal (`cek/uji/`) serta repositori Python open-source `bottle`, lalu memeriksa kesesuaiannya secara manual pada 2 berkas acak.

---

## 5. Rencana Kerja Bertahap & Antisipasi Risiko

* **Tahap 1 (Fondasi & Query):** Setup `.venv` Python + `tugas1-3` (`t1.py`, `jelajah.py`, `q.py`).
* **Tahap 2 (Grammar & Highlighting):** Setup `tree-sitter-cli`, kembangkan `grammar.js` inkremental (`4a`–`4f` + `in`/`contains`), susun `highlights.scm` dan `filter_to_sql.py`.
* **Tahap 3 (CLI Linter & Laporan):** Bangun `cek.py` (Python + pengayaan JS), uji pada repo nyata, susun `README.md` serta `laporan.md`.
* **Antisipasi Risiko:** Menangani perbedaan format ES module (`export default`) pada `tree-sitter 0.27.2`, mengatasi *unresolved conflict* dengan `prec.left`, menjaga decoding karakter (`errors="replace"`), dan mengecualikan direktori vendor/build via `.gitignore`.
