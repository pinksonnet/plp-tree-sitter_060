# Draf Proposal: Pendeteksi Potensi SQL Injection pada Kode Python Web dengan Tree-sitter

Nama: Nazwa Rizqika Azzahra | NIM: 251524060

## 1. Masalah

Pada aplikasi web enterprise berbasis Python (Flask, Django), developer sering membentuk query SQL dengan menyambung string, `%`, `.format()`, atau f-string. Kebiasaan ini membuka celah SQL injection. Pelakunya developer yang menulis kode, dan yang menanggung akibatnya tim keamanan dan reviewer yang harus menemukannya satu per satu saat code review.

## 2. Kenapa tidak cukup dengan AI saja

Meminta AI me-review setiap file hasilnya bisa berbeda tiap kali dijalankan, memakan token per file, dan sulit dijalankan otomatis pada ribuan file di setiap commit. Tool berbasis tree-sitter bersifat deterministik, hampir tanpa biaya per file, dan bisa dipasang di CI. Regex pun tidak cukup: pola teks `execute(...)` ikut menandai komentar dan string biasa, serta salah menandai query yang aman (berparameter) hanya karena ada `%s` di dalamnya. Tree-sitter memahami struktur, sehingga hanya argumen pertama `execute` yang diperiksa.

## 3. Bahasa dan grammar

Python (Flask dan Django), grammar `tree-sitter-python` dari PyPI (versi 0.25.0, sudah dipakai di Tugas 1 sampai 6).

## 4. Contoh kode

Harus terdeteksi:

```python
cursor.execute(f"SELECT * FROM users WHERE id = {uid}")
cursor.execute("SELECT * FROM users WHERE name = '" + nama + "'")
cursor.execute("SELECT * FROM users WHERE id = %s" % uid)
cursor.execute("SELECT * FROM users WHERE id = {}".format(uid))
```

Tidak boleh ikut terdeteksi:

```python
cursor.execute("SELECT * FROM users WHERE id = %s", (uid,))
cursor.execute("SELECT 1")
logger.info(f"user {uid} login")
# cursor.execute(f"SELECT * FROM x WHERE id = {uid}")
```

## 5. Rancangan query

Aturan untuk f-string (dua bentuk lain memakai `binary_operator` dan `call` ke `.format`):

```scheme
(call
  function: (attribute attribute: (identifier) @metode)
  arguments: (argument_list . (string (interpolation)) @sql)
  (#eq? @metode "execute"))
```

Percobaan awal: ketiga pola menandai tepat empat baris pertama pada contoh di atas dan tidak menandai baris yang aman, komentar, maupun string biasa.

## 6. Bentuk output

Laporan di terminal dengan format `file:baris: kemungkinan SQL injection (f-string)`, seperti `cek.py` di Tugas 6. Opsi tambahan: keluaran JSON agar bisa dipakai di CI.

## 7. Cara evaluasi

Repositori uji: `we45/Vulnerable-Flask-App` (sengaja rentan, commit `b6a4f97`) dan satu proyek kuliah sendiri. Hasil diperiksa manual, minimal 20 temuan, untuk menghitung berapa persen yang benar (precision), serta apakah celah yang sudah diketahui ikut terdeteksi (recall). Percobaan awal menunjukkan keterbatasan: pada repo tersebut query langsung menghasilkan 0 temuan, karena kodenya membentuk string lebih dulu ke variabel (`str_query = "..." % search_term`), lalu memanggil `execute(str_query)`.

## 8. Rencana kerja dan risiko

- Minggu 1: tiga pola langsung (f-string, `+`, `%`/`.format`) beserta kasus uji benar dan salah.
- Minggu 2: pola tidak langsung, yaitu string dibentuk ke variabel lalu dipakai di `execute`, dengan query dan sedikit kode Python di dalam satu fungsi.
- Minggu 3: uji pada repositori nyata, hitung precision dan recall, perbaiki aturan.
- Minggu 4: keluaran JSON, README, dan laporan.

Risiko: query tidak bisa melacak aliran data antar fungsi, sehingga sebagian celah tidak terdeteksi. Cakupan akan dibatasi dan dijelaskan di laporan.