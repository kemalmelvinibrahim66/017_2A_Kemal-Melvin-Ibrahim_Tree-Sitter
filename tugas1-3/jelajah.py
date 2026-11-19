import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah_rekursif(node, kedalaman=0, field=None, hasil=None):
    if hasil is None:
        hasil = []
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    hasil.append("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    for i, child in enumerate(node.children):
        if not child.is_named:
            continue
        jelajah_rekursif(child, kedalaman + 1, node.field_name_for_child(i), hasil)
    return hasil


def jelajah_cursor(tree):
    hasil = []
    cursor = tree.walk()
    kedalaman = 0
    sudah_kunjungi_anak = False

    while True:
        if not sudah_kunjungi_anak:
            node = cursor.node
            if node.is_named:
                baris, kolom = node.start_point
                field = cursor.field_name
                label = f"{field}: " if field else ""
                hasil.append("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
                if cursor.goto_first_child():
                    kedalaman += 1
                    continue

        if cursor.goto_next_sibling():
            sudah_kunjungi_anak = False
            continue

        if cursor.goto_parent():
            kedalaman -= 1
            sudah_kunjungi_anak = True
            continue

        break

    return hasil


if __name__ == "__main__":
    target = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else ""

    with open(target, "rb") as f:
        tree = parser.parse(f.read())

    if mode == "--cursor":
        print("\n".join(jelajah_cursor(tree)))
    elif mode == "--cek":
        out_rekursif = jelajah_rekursif(tree.root_node)
        out_cursor = jelajah_cursor(tree)
        sama = out_rekursif == out_cursor
        print(f"File: {target}")
        print(f"Baris rekursif : {len(out_rekursif)}")
        print(f"Baris TreeCursor: {len(out_cursor)}")
        print(f"Output identik : {sama}")
    else:
        print("\n".join(jelajah_rekursif(tree.root_node)))