import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

FOLDER_DIABAIKAN = {".venv", "venv", ".git", "node_modules", "__pycache__"}
Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')


def cek_file(path: Path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO] {path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2 (TODO): fungsi yang lebih dari 30 baris
    # Fitur 3 (TODO): file yang pohonnya mengandung error


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Pemakaian: python cek.py <folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    for path in sorted(target.rglob("*.py")):
        if any(part in FOLDER_DIABAIKAN for part in path.parts):
            continue
        cek_file(path)