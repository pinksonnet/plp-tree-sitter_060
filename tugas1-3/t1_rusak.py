import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

rusak = {
    "tanpa_titik_dua": b"def sapa(nama)\n    return nama\n",
    "tanpa_kurung_tutup": b"def sapa(nama:\n    return nama\n",
}

for judul, kode in rusak.items():
    tree = parser.parse(kode)
    print("Potongan:", judul)
    print(tree.root_node)
    print()