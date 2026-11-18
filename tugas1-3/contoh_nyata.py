import json
import sys


class Mahasiswa:
    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self.nilai = {}

    def tambah_nilai(self, mata_kuliah, angka):
        if angka < 0 or angka > 100:
            raise ValueError("Nilai harus 0 sampai 100")
        self.nilai[mata_kuliah] = angka

    def rata_rata(self):
        if not self.nilai:
            return 0
        total = 0
        for angka in self.nilai.values():
            total += angka
        return total / len(self.nilai)

    def huruf_mutu(self):
        rata = self.rata_rata()
        if rata >= 85:
            return "A"
        elif rata >= 70:
            return "B"
        elif rata >= 55:
            return "C"
        elif rata >= 40:
            return "D"
        else:
            return "E"


class DaftarMahasiswa:
    def __init__(self):
        self.data = []

    def tambah(self, mahasiswa):
        for item in self.data:
            if item.nim == mahasiswa.nim:
                raise ValueError("NIM sudah terdaftar")
        self.data.append(mahasiswa)

    def cari(self, nim):
        for item in self.data:
            if item.nim == nim:
                return item
        return None

    def hapus(self, nim):
        target = self.cari(nim)
        if target is None:
            return False
        self.data.remove(target)
        return True

    def urut_rata_rata(self):
        return sorted(self.data, key=lambda m: m.rata_rata(), reverse=True)

    def simpan(self, path):
        isi = []
        for item in self.data:
            isi.append({"nim": item.nim, "nama": item.nama, "nilai": item.nilai})
        with open(path, "w") as f:
            json.dump(isi, f, indent=2)

    def muat(self, path):
        with open(path) as f:
            isi = json.load(f)
        self.data = []
        for baris in isi:
            mahasiswa = Mahasiswa(baris["nim"], baris["nama"])
            mahasiswa.nilai = baris["nilai"]
            self.data.append(mahasiswa)


def cetak_laporan(daftar):
    print("Laporan nilai mahasiswa")
    print("-" * 30)
    nomor = 1
    for item in daftar.urut_rata_rata():
        rata = item.rata_rata()
        print(f"{nomor}. {item.nama} ({item.nim}) {rata:.1f} {item.huruf_mutu()}")
        nomor += 1


def hitung_statistik(daftar):
    if not daftar.data:
        return {"jumlah": 0, "tertinggi": 0, "terendah": 0}
    rata_semua = [m.rata_rata() for m in daftar.data]
    return {
        "jumlah": len(rata_semua),
        "tertinggi": max(rata_semua),
        "terendah": min(rata_semua),
    }


def main():
    daftar = DaftarMahasiswa()
    ani = Mahasiswa("2301", "Ani")
    ani.tambah_nilai("Struktur Data", 88)
    ani.tambah_nilai("Basis Data", 76)
    budi = Mahasiswa("2302", "Budi")
    budi.tambah_nilai("Struktur Data", 60)
    budi.tambah_nilai("Basis Data", 52)
    daftar.tambah(ani)
    daftar.tambah(budi)
    cetak_laporan(daftar)
    statistik = hitung_statistik(daftar)
    print(statistik)
    if len(sys.argv) > 1:
        daftar.simpan(sys.argv[1])


if __name__ == "__main__":
    main()