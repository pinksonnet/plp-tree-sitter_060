import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')

Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

BATAS_BARIS = 30

def cari_error(node):
    if not node.has_error:
        return None
    if node.is_error or node.is_missing:
        return node
    for anak in node.children:
        hasil = cari_error(anak)
        if hasil:
            return hasil
    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > BATAS_BARIS:
            print(f"{path}:{fungsi.start_point[0] + 1}: fungsi {nama} {jumlah} baris")

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        masalah = cari_error(tree.root_node)
        jenis = "MISSING" if masalah.is_missing else "ERROR"
        print(f"{path}:{masalah.start_point[0] + 1}: sintaks bermasalah ({jenis})")

for path in sorted(Path(sys.argv[1]).rglob("*.py")):
    cek_file(path)