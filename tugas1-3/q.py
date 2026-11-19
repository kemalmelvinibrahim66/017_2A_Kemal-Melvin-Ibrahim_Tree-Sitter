import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2], encoding="utf-8").read()
mode = sys.argv[3] if len(sys.argv) > 3 else ""

tree = parser.parse(kode)
cursor = QueryCursor(Query(PY, pola))

if mode == "--fungsi":
    for _, cap in cursor.matches(tree.root_node):
        nama_nodes = cap.get("nama", [])
        params_nodes = cap.get("params", [])
        if nama_nodes and params_nodes:
            nama = nama_nodes[0].text.decode()
            jumlah = params_nodes[0].named_child_count
            baris = nama_nodes[0].start_point[0] + 1
            print(f"{nama} ({jumlah} parameter) [baris {baris}]")
elif mode == "--matches":
    for idx, (_, cap) in enumerate(cursor.matches(tree.root_node), 1):
        bagian = []
        for label, nodes in cap.items():
            for n in nodes:
                teks = n.text.decode(errors="replace").strip()
                bagian.append(f"@{label}={teks!r} (baris {n.start_point[0] + 1})")
        print(f"Match {idx}: " + " | ".join(bagian))
else:
    hasil = cursor.captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in sorted(nodes, key=lambda x: x.start_byte):
            teks = n.text.decode(errors="replace").strip()
            print(f"@{nama}  baris {n.start_point[0] + 1}: {teks}")