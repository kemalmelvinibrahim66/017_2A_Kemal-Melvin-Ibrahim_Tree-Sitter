# `cek.py` — Pendeteksi TODO, Fungsi Panjang, dan Syntax Error

CLI berbasis **Tree-sitter** untuk memindai seluruh berkas **Python (`.py`)** dan **JavaScript (`.js`)** di dalam suatu folder secara rekursif.

## Fitur

1. **Deteksi Komentar `TODO` / `FIXME`**  
   Menggunakan Tree-sitter Query (`((comment) @c (#match? @c "TODO|FIXME"))`) sehingga hanya memeriksa node komentar asli—teks `"TODO"` di dalam string literal tidak ikut terlaporkan.
2. **Deteksi Fungsi Panjang (`> 30` baris)**  
   Menghitung jumlah baris fungsi dari `end_point[0] - start_point[0] + 1`:
   * **Python:** `function_definition`
   * **JavaScript:** `function_declaration`, `method_definition`, `arrow_function`, dan `function_expression`
3. **Deteksi Syntax Error**  
   Memeriksa `tree.root_node.has_error`, lalu menelusuri pohon secara rekursif untuk melaporkan posisi baris pertama node `is_error` atau `is_missing`.

## Catatan Perilaku & Batasan

* **Semua fungsi dihitung**, termasuk method di dalam kelas maupun fungsi bersarang (*nested function*).
* Folder `.venv`, `venv`, `.git`, `node_modules`, dan `__pycache__` dilewati secara otomatis.
* Pembacaan teks menggunakan `decode(errors="replace")` agar aman terhadap perbedaan encoding berkas.

## Cara Memasang Dependensi

Butuh **Python 3.10+**. Dari folder root repositori:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Atau pasang langsung paket yang dibutuhkan `cek.py`:

```bash
pip install tree-sitter tree-sitter-python tree-sitter-javascript
```

## Cara Menjalankan

```powershell
# Dari folder root repositori
python cek/cek.py <folder_target>

# Contoh pada folder uji lokal
python cek/cek.py cek/uji

# Contoh pada repositori eksternal
python cek/cek.py ..\bottle
```

## Contoh Output

Hasil pada folder lokal `cek/uji`:

```text
[TODO] cek\uji\ada_todo.py:1: # TODO: rapikan pesan sambutan
[TODO] cek\uji\ada_todo.py:3: # FIXME: validasi jika nama kosong
[TODO] cek\uji\contoh.js:1: // TODO: rapikan fungsi hitung
[PANJANG] cek\uji\contoh.js:4: fungsi 'prosesPanjangJS' (33 baris)
[PANJANG] cek\uji\fungsi_panjang.py:5: fungsi 'proses_panjang' (32 baris)
[ERROR] cek\uji\rusak.js:1: file mengandung syntax error
[ERROR] cek\uji\sintaks_rusak.py:1: file mengandung syntax error
```

Hasil lengkap pengujian pada repositori open-source [bottle](https://github.com/bottlepy/bottle) (26 temuan) beserta verifikasi manual 2 berkas acak tersedia di [`cek/output_t6.txt`](./output_t6.txt).
