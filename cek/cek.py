import sys
from pathlib import Path
import tree_sitter_javascript as tsjs
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY_LANG = Language(tspython.language())
JS_LANG = Language(tsjs.language())

FOLDER_DIABAIKAN = {".venv", "venv", ".git", "node_modules", "__pycache__"}

KONFIG_BAHASA = {
    ".py": (
        Parser(PY_LANG),
        Query(PY_LANG, '((comment) @c (#match? @c "TODO|FIXME"))'),
        Query(PY_LANG, "(function_definition name: (identifier) @nama) @fungsi"),
    ),
    ".js": (
        Parser(JS_LANG),
        Query(JS_LANG, '((comment) @c (#match? @c "TODO|FIXME"))'),
        Query(
            JS_LANG,
            """
            (function_declaration name: (identifier) @nama) @fungsi
            (method_definition name: (property_identifier) @nama) @fungsi
            (variable_declarator
              name: (identifier) @nama
              value: [(arrow_function) (function_expression)] @fungsi)
            """,
        ),
    ),
}


def cari_error_pertama(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error_pertama(child)
        if hasil is not None:
            return hasil
    return None


def cek_file(path: Path):
    parser, q_todo, q_fungsi = KONFIG_BAHASA[path.suffix]
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(q_todo).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO] {path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi lebih dari 30 baris
    for _, cap in QueryCursor(q_fungsi).matches(tree.root_node):
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Pemakaian: python cek.py <folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    for path in sorted(target.rglob("*")):
        if path.suffix not in KONFIG_BAHASA or not path.is_file():
            continue
        if any(part in FOLDER_DIABAIKAN for part in path.parts):
            continue
        cek_file(path)