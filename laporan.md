# Laporan Tugas Awal Tree-sitter (Tugas 1–6)

* **Nama:** Kemal Melvin Ibrahim
* **NIM / Kelas:** 017 / 2A
* **Mata Kuliah:** Programming Language Pragmatics (PLP)

---

## 1. Ringkasan Tugas dan Bukti Hasil (Output Teks)

### Tugas 1 — Membaca Pohon (`tugas1-3/t1.py`, `tugas1-3/output_t1.txt`)
Mem-parse 3 potongan kode Python pendek (fungsi, `if`/`else`, dan kelas dengan 1 method), membandingkan pohon perkiraan dengan hasil aktual `tree.root_node`, mengidentifikasi perbedaan `children` vs `named_children`, serta menguji *error recovery* dengan menghapus tanda `:` setelah `def sapa(nama)`.

* **Temuan utama:** Node `(string)` pada `tree-sitter-python` memiliki 3 child bernama (`string_start`, `string_content`, `string_end`), sedangkan `comparison_operator` tidak memakai label `left:`/`right:` seperti `binary_operator`. Token literal seperti `def`, `:`, `(`, `)` tersimpan sebagai node anonim (`is_named == False`).
* **Cuplikan hasil terminal (inspeksi node anonim & *error recovery*):**

```text
--- Anak function_definition (children) ---
def -> anonim
identifier -> bernama
parameters -> bernama
: -> anonim
block -> bernama

--- Anak parameters (children) ---
( -> anonim
identifier -> bernama
) -> anonim

has_error: True
(module (ERROR (identifier) (parameters (identifier)) (expression_statement (binary_operator left: (string (string_start) (string_content) (string_end)) right: (identifier)))))
```

### Tugas 2 — Penjelajah Node (`tugas1-3/jelajah.py`, `tugas1-3/output_t2.txt`)
Mengimplementasikan penelusuran DFS rekursif untuk mencetak node bernama beserta kedalaman indentasi, posisi `[baris:kolom]`, dan nama field (`node.field_name_for_child(i)` memakai indeks `node.children`). Diuji bertahap dari `kecil.py` (1 baris) hingga berkas nyata `analyzer.py` (102 baris, menghasilkan 828 baris node di `output_t2_analyzer.txt`). Sebagai pengayaan, ditambahkan versi `TreeCursor` (`--cursor` dan `--cek`).

```text
$ python tugas1-3/jelajah.py tugas1-3/kecil.py
module [1:0]
  expression_statement [1:0]
    assignment [1:0]
      left: identifier [1:0]
      right: integer [1:4]

$ python tugas1-3/jelajah.py tugas1-3/analyzer.py --cek
File: tugas1-3/analyzer.py
Baris rekursif : 828
Baris TreeCursor: 828
Output identik : True
```

### Tugas 3 — Query Pertama (`tugas1-3/q.py`, `*.scm`, `tugas1-3/output_t3.txt`)
Menulis query deklaratif `.scm` dengan `Query` dan `QueryCursor`: `fungsi.scm` (nama fungsi & `named_child_count` via `matches`), `print.scm` (predikat `#eq?`), `import.scm` (pola `import_statement`, `aliased_import`, `import_from_statement`, dan `relative_import` dari inspeksi `jelajah.py`), serta pengayaan `docstring.scm` memakai *anchor* anak pertama (`.`).

```text
=== UJI PADA analyzer.py ===
analyze_statement (1 parameter) [baris 7]
_collect_select (3 parameter) [baris 31]
_collect (3 parameter) [baris 50]
column_usage (1 parameter) [baris 78]
reads (1 parameter) [baris 83]
@modul  baris 2: collections
@modul  baris 4: .
Match 1: @fn='analyze_statement' (baris 7) | @docstring='"""Mengembalikan {nama_tabel: {operasi}} untuk satu statement."""' (baris 8)
Match 2: @fn='_collect_select' (baris 31) | @docstring='"""Menandai semua tabel di SELECT (termasuk subquery-nya) dengan `op`."""' (baris 32)
Match 3: @fn='_collect' (baris 50) | @docstring='"""Menandai tabel di setiap subquery di dalam ekspresi dengan `op`."""' (baris 51)
Match 4: @fn='column_usage' (baris 78) | @docstring='"""Penggunaan kolom (tabel, kolom, operasi). Membutuhkan resolver sudah\r\n    dijalankan, karena memakai ColumnRef.resolved."""' (baris 79)
```
*(Cocok dengan hitungan manual pada `analyzer.py`: 5 fungsi, 0 pemanggilan `print()`, 2 statement import, dan 4 docstring).*

### Tugas 4 — Grammar DSL Filter (`tree-sitter-filter/`, `filter_to_sql.py`, `output_t4.txt`)
Membangun grammar DSL `filter` secara inkremental (`4a`–`4f`) dengan `word: $ => $.identifier`, prioritas operator (`not` 3 > `and` 2 > `or` 1), tanda kurung `parenthesized`, label `field(...)`, `in_expression` + `value_list`, serta operator `contains`. Sebagai pengayaan, skrip `filter_to_sql.py` mengubah AST `filter` menjadi klausa SQL `WHERE` berparameter `?` agar aman dari *SQL injection*.

```text
$ tree-sitter test
  dasar:
      1. ✓ perbandingan dengan string
      2. ✓ perbandingan dengan angka
      3. ✓ ekspresi and
      4. ✓ and lebih kuat dari or
      5. ✓ tanda kurung mengubah prioritas
      6. ✓ not expression dan boolean
      7. ✓ ekspresi in dengan tiga nilai
      8. ✓ ekspresi contains
Total parses: 8; successful parses: 8; failed parses: 0; success percentage: 100.00%

$ python tree-sitter-filter/filter_to_sql.py
Input : status = "open" and (priority >= 2 or title contains "invoice")
SQL   : WHERE status = ? AND (priority >= ? OR title LIKE ?)
Params: ['open', 2, '%invoice%']
Input : owner = "budi' OR '1'='1"
SQL   : WHERE owner = ?
Params: ["budi' OR '1'='1"]
```

### Tugas 5 — Syntax Highlighting DSL Filter (`queries/highlights.scm`, `tree-sitter.json`, `output_t5.txt`)
Mengonfigurasi `tree-sitter init-config` (`parser-directories`), menambahkan `"highlights": "queries/highlights.scm"` di `tree-sitter.json`, serta memetakan capture `@keyword` (`and`, `or`, `not`, `in`, `contains`), `@operator`, `@string`, `@number`, `@constant.builtin`, `@property` (pada `comparison` dan `in_expression`), serta `@punctuation.*`.

```text
$ tree-sitter highlight --check contoh.filter
All highlight captures conform to standards.

$ tree-sitter query queries/highlights.scm contoh.filter
contoh.filter
  pattern: 6 -> capture: 5 - property, start: (0, 0), end: (0, 6), text: `status`
  pattern: 0 -> capture: 0 - keyword, start: (0, 7), end: (0, 9), text: `in`
  pattern: 2 -> capture: 2 - string, start: (0, 11), end: (0, 17), text: `"open"`
  ...
  pattern: 5 -> capture: 5 - property, start: (0, 48), end: (0, 56), text: `priority`
  pattern: 1 -> capture: 1 - operator, start: (0, 57), end: (0, 59), text: `>=`
  pattern: 3 -> capture: 3 - number, start: (0, 60), end: (0, 61), text: `2`
  pattern: 0 -> capture: 0 - keyword, start: (0, 71), end: (0, 79), text: `contains`
  pattern: 4 -> capture: 4 - constant.builtin, start: (0, 110), end: (0, 114), text: `true`
```

### Tugas 6 — Mini Proyek CLI `cek.py` (`cek/cek.py`, `cek/README.md`, `cek/output_t6.txt`)
Membangun CLI `cek.py <folder>` untuk mendeteksi komentar `TODO`/`FIXME`, fungsi $> 30$ baris, dan berkas ber-error (`has_error` + baris error pertama via `cari_error_pertama`), dengan melewati `.venv`, `venv`, `.git`, `node_modules`, dan `__pycache__`. Dilengkapi pengayaan dukungan `.js` (`tree-sitter-javascript`) lewat pemetaan `KONFIG_BAHASA`.

```text
$ python cek/cek.py cek/uji
[TODO] cek\uji\ada_todo.py:1: # TODO: rapikan pesan sambutan
[TODO] cek\uji\ada_todo.py:3: # FIXME: validasi jika nama kosong
[TODO] cek\uji\contoh.js:1: // TODO: rapikan fungsi hitung
[PANJANG] cek\uji\contoh.js:4: fungsi 'prosesPanjangJS' (33 baris)
[PANJANG] cek\uji\fungsi_panjang.py:5: fungsi 'proses_panjang' (32 baris)
[ERROR] cek\uji\rusak.js:1: file mengandung syntax error
[ERROR] cek\uji\sintaks_rusak.py:1: file mengandung syntax error
```

* **Uji repo nyata (`https://github.com/bottlepy/bottle`):** menghasilkan 26 temuan. Verifikasi manual 2 berkas acak cocok 100%: `test/test_html_helper.py` (1 TODO di baris 8, 0 fungsi panjang, 0 error) dan `test/test_config.py` (0 TODO, 1 fungsi panjang `test_overlay` baris 106–166 = 61 baris, 0 error).

---

## 2. Kendala dan Cara Mengatasinya

| No | Kendala yang Ditemui | Penyebab | Solusi |
| :---: | :--- | :--- | :--- |
| 1 | `ReferenceError: module is not defined in ES module scope` saat `tree-sitter generate` | CLI `tree-sitter 0.27.2` membuat `package.json` dengan `"type": "module"`, sedangkan contoh panduan memakai CommonJS (`module.exports`). | Mengubah baris pembuka `grammar.js` menjadi `export default grammar({ ... })`. |
| 2 | `pip install -e ./tree-sitter-filter` gagal (`project.urls.Funding must be url`) | Template `tree-sitter init` menulis `Funding = ""` di `pyproject.toml`, belum ada `README.md`, dan `.gitignore` belum memblokir `*.pyd`. | Menghapus `Funding = ""`, membuat `README.md`, dan menambahkan `*.pyd` ke `.gitignore`. |
| 3 | Tes `contains` gagal sebagai `(ERROR (identifier) (identifier) (string))` | `tree-sitter generate` belum dijalankan ulang setelah `'contains'` ditambahkan ke `grammar.js`. | Menjalankan `tree-sitter generate` lalu `tree-sitter test` hingga 8/8 lulus. |
| 4 | Token `status` pada `status in (...)` tidak ikut berwarna saat highlight | `highlights.scm` hanya menarget `(comparison field: (identifier) @property)`, belum mencakup `in_expression`. | Menambahkan rule `(in_expression field: (identifier) @property)`. |
| 5 | `NameError: name 'cari_error_pertama' is not defined` di `cek.py` | Definisi fungsi diletakkan di bawah blok `if __name__ == "__main__":`. | Memindahkan `cari_error_pertama` ke atas blok pemanggilan utama. |

---

## 3. Catatan Penggunaan AI

AI dipakai sebagai pendamping debugging, pembuatan kerangka kode, dan perapian dokumentasi. Setiap hasil tetap diuji ulang sebelum di-commit:

| Bagian | Yang Diminta ke AI | Kekurangan / Koreksi yang Ditemukan | Bukti Verifikasi |
| :--- | :--- | :--- | :--- |
| **Tugas 1–3** | Format `output_t1.txt`, kerangka `TreeCursor`, dan variasi query `.scm`. | Di awal `output_t1.txt` sempat salah tempel output `x = 1 + 2` di bagian fungsi, dan tebakan awal `(string)` sebagai node daun berbeda dari pohon asli. | Menjalankan ulang `t1.py`, cek `--cek` pada `analyzer.py` (828 baris identik), serta hitung manual hasil query di `contoh_q.py` dan `analyzer.py`. |
| **Tugas 4–5** | Panduan `grammar.js`, skrip `filter_to_sql.py`, dan `highlights.scm`. | Contoh `module.exports` error di `tree-sitter 0.27.2` (harus `export default`), dan `pip install -e` sempat gagal karena `Funding = ""` di `pyproject.toml`. | Terlihat dari error `ReferenceError` saat `tree-sitter generate` dan `ValueError` dari `setuptools`, serta 8/8 tes corpus lulus setelah diperbaiki. |
| **Tugas 6** | Kerangka `cek.py`, dukungan `.js`, dan `README.md`. | `requirements.txt` sempat belum menyertakan `tree-sitter-javascript==0.25.0` setelah pengayaan `.js` ditambahkan. | Dicek langsung di `requirements.txt`, uji ulang `cek/uji`, dan cek manual 2 berkas di repo `bottle`. |
| **Dokumentasi** | Kerangka dokumentasi tugas. | Masih banyak yang belum rapih. | Dicek langsung secara manual oleh saya. |
