import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

potongan = {
    "assignment": b"x = 1\n",
    "fungsi": b"def tambah(a, b):\n    return a + b\n",
    "if_else": b'if x > 0:\n    print("positif")\nelse:\n    print("non positif")\n',
    "kelas": b'class Mahasiswa:\n    def sapa(self):\n        return "Halo"\n',
}


def cetak_anak(node):
    for anak in node.children:
        status = "bernama" if anak.is_named else "anonim"
        print("  ", anak.type, status)


for judul, kode in potongan.items():
    tree = parser.parse(kode)
    print("Potongan:", judul)
    print(kode.decode())
    print(tree.root_node)
    print("Anak dari", tree.root_node.children[0].type)
    cetak_anak(tree.root_node.children[0])
    print()

tree = parser.parse(potongan["fungsi"])
fungsi = tree.root_node.children[0]
parameters = fungsi.child_by_field_name("parameters")
print("Anak dari parameters")
cetak_anak(parameters)
print()

print("children vs named_children dari function_definition")
print("children:", [anak.type for anak in fungsi.children])
print("named_children:", [anak.type for anak in fungsi.named_children])
print("jumlah children:", len(fungsi.children))
print("jumlah named_children:", len(fungsi.named_children))
print()

tree = parser.parse(potongan["if_else"])
if_node = tree.root_node.children[0]
else_clause = if_node.child_by_field_name("alternative")
print("Anak dari else_clause")
cetak_anak(else_clause)