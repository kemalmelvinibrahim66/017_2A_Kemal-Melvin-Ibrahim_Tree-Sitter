import tree_sitter_python as tspython 
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

# kode = b"""if nilai >= 75:
#     status = "Lulus"
# else:
#     status = "Ulang"
# """

# kode = b"""class Mahasiswa:
#     def halo(self):
#         return "Halo"
# """

kode = b"""def sapa(nama)
    return "Halo " + nama
"""
tree = parser.parse(kode)
print("has_error:", tree.root_node.has_error)
print(tree.root_node)

fn = tree.root_node.children[0]
print("\n--- Anak root_node.children[0] ---")
for c in fn.children:
    print(c.type, "-> bernama" if c.is_named else "-> anonim")
    
params = fn.child_by_field_name("parameters")
if params:
    print("\n--- Anak parameters (children) ---")
    for c in params.children:
        print(c.type, "-> bernama" if c.is_named else "-> anonim")