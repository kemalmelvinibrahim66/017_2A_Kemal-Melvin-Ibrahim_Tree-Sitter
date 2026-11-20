import tree_sitter_filter as tsfilter
from tree_sitter import Language, Parser

FILTER_LANG = Language(tsfilter.language())
parser = Parser(FILTER_LANG)


def _ambil_nilai(node):
    teks = node.text.decode("utf-8")
    if node.type == "string":
        return teks[1:-1]  # buang tanda kutip " di awal & akhir
    if node.type == "number":
        return float(teks) if "." in teks else int(teks)
    if node.type == "boolean":
        return teks == "true"
    raise ValueError(f"Tipe nilai tidak dikenal: {node.type}")


def _bangun_sql(node, params):
    tipe = node.type

    if tipe == "query":
        return _bangun_sql(node.named_children[0], params)

    if tipe == "parenthesized":
        isi = _bangun_sql(node.named_children[0], params)
        return f"({isi})"

    if tipe == "not_expression":
        operand = _bangun_sql(node.child_by_field_name("operand"), params)
        return f"NOT ({operand})"

    if tipe == "and_expression":
        kiri = _bangun_sql(node.child_by_field_name("left"), params)
        kanan = _bangun_sql(node.child_by_field_name("right"), params)
        return f"{kiri} AND {kanan}"

    if tipe == "or_expression":
        kiri = _bangun_sql(node.child_by_field_name("left"), params)
        kanan = _bangun_sql(node.child_by_field_name("right"), params)
        return f"{kiri} OR {kanan}"

    if tipe == "comparison":
        kolom = node.child_by_field_name("field").text.decode("utf-8")
        op = node.child_by_field_name("operator").text.decode("utf-8")
        nilai = _ambil_nilai(node.child_by_field_name("value"))

        if op == "contains":
            params.append(f"%{nilai}%")
            return f"{kolom} LIKE ?"

        params.append(nilai)
        return f"{kolom} {op} ?"

    if tipe == "in_expression":
        kolom = node.child_by_field_name("field").text.decode("utf-8")
        daftar = node.child_by_field_name("values").named_children
        placeholders = ", ".join("?" for _ in daftar)
        for item in daftar:
            params.append(_ambil_nilai(item))
        return f"{kolom} IN ({placeholders})"

    raise ValueError(f"Node tidak didukung: {tipe}")


def filter_ke_sql(teks_filter: str):
    tree = parser.parse(teks_filter.encode("utf-8"))
    if tree.root_node.has_error:
        raise ValueError("Sintaks filter tidak valid")

    params = []
    where_clause = _bangun_sql(tree.root_node, params)
    return f"WHERE {where_clause}", params


if __name__ == "__main__":
    contoh = [
        'status = "open" and (priority >= 2 or title contains "invoice")',
        'status in ("open", "pending", "closed") and not archived = true',
        'owner = "budi\' OR \'1\'=\'1"',
    ]

    for teks in contoh:
        sql, params = filter_ke_sql(teks)
        print("Input :", teks)
        print("SQL   :", sql)
        print("Params:", params)
        print("-" * 60)