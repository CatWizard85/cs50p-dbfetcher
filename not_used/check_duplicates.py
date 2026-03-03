from dbfread import DBF

art_col_map = {
    "AA_CODART" : "codart",
    "AA_DESCR1" : "descr1",
    "AA_DESCR2" : "descr2",
    "AA_UNIMIS" : "um",
    "AA_USER2" : "fsc_1",
    "AA_USER3" : "fsc_2",
}

lotto_col_map = {
    "TC_CODART": "codart",
    "TC_TAGCOL": "cod_lotto",
}

def filter_columns(table, columns):
    if isinstance(columns, dict):
        cols = set(columns.keys())
    else:
        cols = set(columns)  # lista o tuple

    for record in table:
        yield {k: v for k, v in record.items() if k in cols}

seen = set()
duplicati = False
for record in filter_columns(DBF("ANAART.dbf", encoding="latin1"), art_col_map):
    cod = record["AA_CODART"].ljust(25)
    if cod in seen:
        print(f"Duplicato: -{cod}-")
        duplicati = True
    seen.add(cod)

if not duplicati:
    print("Nessun duplicato")
