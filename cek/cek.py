import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

FOLDER_DIABAIKAN = {".venv", "venv", ".git", "node_modules", "__pycache__"}
Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")


def cek_file(path: Path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO] {path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        nama_nodes = cap.get("nama", [])
        fungsi_nodes = cap.get("fungsi", [])
        if not nama_nodes or not fungsi_nodes:
            continue
        fn = fungsi_nodes[0]
        nama = nama_nodes[0].text.decode(errors="replace")
        jumlah_baris = fn.end_point[0] - fn.start_point[0] + 1
        if jumlah_baris > 30:
            print(f"[PANJANG] {path}:{fn.start_point[0] + 1}: fungsi '{nama}' ({jumlah_baris} baris)")

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        err = cari_error_pertama(tree.root_node)
        baris = err.start_point[0] + 1 if err else 1
        print(f"[ERROR] {path}:{baris}: file mengandung syntax error")

def cari_error_pertama(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error_pertama(child)
        if hasil is not None:
            return hasil
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Pemakaian: python cek.py <folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    for path in sorted(target.rglob("*.py")):
        if any(part in FOLDER_DIABAIKAN for part in path.parts):
            continue
        cek_file(path)