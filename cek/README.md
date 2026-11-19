# cek

Alat baris perintah untuk memeriksa folder berisi file Python dengan tree-sitter.

## Fitur

1. Melaporkan komentar yang mengandung TODO atau FIXME beserta file dan barisnya.
2. Melaporkan fungsi yang lebih dari 30 baris.
3. Melaporkan file yang pohon sintaksnya mengandung error, beserta baris pertama yang bermasalah.

## Memasang

```
pip install tree-sitter tree-sitter-python
```

## Menjalankan

```
python cek.py <folder>
```

Contoh (dijalankan dari folder `cek`):

```
python cek.py uji
```

## Contoh output

```
uji/panjang.py:1: fungsi proses 38 baris
uji/rusak.py:1: sintaks bermasalah (ERROR)
uji/todo.py:2: # TODO: tangani pembagian dengan nol
uji/todo.py:7: # FIXME: nama kosong belum dicek
```

Format tiap baris: `file:baris: keterangan`. Di Windows pemisah path berupa `\`.

## Catatan

- Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.
- Panjang fungsi dihitung dari baris `def` sampai baris terakhir fungsi.
- Untuk file yang rusak, hanya baris pertama yang bermasalah yang dilaporkan.
- Hanya file berekstensi `.py` yang diperiksa.

## Pengujian

Diuji pada repositori `pallets/itsdangerous` (commit `672971d`, 15 file Python). Hasilnya 1 komentar TODO, 6 fungsi lebih dari 30 baris, dan tidak ada file dengan error. Hasil tersebut dicocokkan secara manual pada dua file (`timed.py` dan `signer.py`).