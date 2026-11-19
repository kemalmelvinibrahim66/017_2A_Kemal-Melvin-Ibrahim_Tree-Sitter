import tree_sitter_python as tspython 
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"""def sapa(nama):
    return "Halo " + nama
"""

kode = b"""if nilai >= 75:
    status = "Lulus"
else:
    status = "Ulang"
"""

tree = parser.parse(kode)
print(tree.root_node)