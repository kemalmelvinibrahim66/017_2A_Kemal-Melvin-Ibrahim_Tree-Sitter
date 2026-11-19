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

kode = b"""def sapa(nama):
    return "Halo " + nama
"""
tree = parser.parse(kode)
print(tree.root_node)

fn = tree.root_node.children[0]
print("\n--- Anak function_definition (children) ---")
for c in fn.children:
    print(c.type, "-> bernama" if c.is_named else "-> anonim")

params = fn.child_by_field_name("parameters")
print("\n--- Anak parameters (children) ---")
for c in params.children:
    print(c.type, "-> bernama" if c.is_named else "-> anonim")
    
print("\n--- Hanya named_children di function_definition ---")
for c in fn.named_children:
    print(c.type)