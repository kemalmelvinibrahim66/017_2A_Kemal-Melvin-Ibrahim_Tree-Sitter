import tree_sitter_python as tspython 
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def sapa(nama):
    return "Halo " + nama

kode = b"""def sapa(nama):
    return "Halo " + nama
"""
tree = parser.parse(kode)
print(tree.root_node)