import sqlite3
import time
import sys
from dbfread import DBF
from .cliente import Cliente
from .fornitore import Fornitore
from .movimento import Movimento
from .articolo import Articolo
from .lotto import Lotto
from config import DB_PATH, DBF_DIR


""" LISTS AND DICTIONARIES TO MAP DATA """


art_col_map = {
    "AA_CODART" : "codart",
    "AA_DESCR1" : "descr1",
    "AA_DESCR2" : "descr2",
    "AA_UNIMIS" : "um",
    "AA_USER2" : "fsc_1",
    "AA_USER3" : "fsc_2",
}

ubic_col_map = {
    "IM_CODART" : "codart",
    "IM_TAGCOL" : "cod_lotto",
    "IM_UBICAZ" : "ubicazione",
}

mov_col_map = {
    "MM_RECORD" : "record",
    "MM_DATDOC" : "data",
    "MM_CODCAU" : "tipo_doc",
    "MM_NUMDOC" : "num_doc",
    "MM_ALIAS" : "cod_clifor",
    "MM_CODART" : "codart",
    "MM_TAGCOL" : "cod_lotto",
    "MM_DESCR1" : "descr1",
    "MM_DESCR2" : "descr2",
    "MM_UNIMIS" : "um",
    "MM_QUANTI" : "quantita",
    "MM_PREZZO" : "prezzo",
}

lotto_col_map = {
    "TC_CODART": "codart",
    "TC_TAGCOL": "cod_lotto",
}

clie_col_map = {
    "SO_ALIAS": "cod_clie",
    "SO_DESSOT": "nome",
    "SO_NUMTEL": "num_tel",
    "SO_INDIRI": "indirizzo",
    "SO_LOCALI": "citta",
    "SO_PROVIN": "provincia",
}

forn_col_map = {
    "SO_ALIAS": "cod_forn",
    "SO_DESSOT": "nome",
    "SO_NUMTEL": "num_tel",
    "SO_INDIRI": "indirizzo",
    "SO_LOCALI": "citta",
    "SO_PROVIN": "provincia",
}

numeric_fields = ["MM_RECORD", "MM_NUMDOC", "MM_QUANTI", "MM_PREZZO"]
giac_fields = ["PM_ANNRIF", "PM_CODART", "PM_TAGCOL", "PM_QTAINI", "PM_QTAACQ", "PM_QTACAR", "PM_QTAVEN", "PM_QTASCA"]
ubic_fields = ["IM_CODART", "IM_TAGCOL", "IM_UBICAZ"]
codart_fields = ["AA_CODART", "IM_CODART", "MM_CODART", "TC_CODART", "PM_CODART"]
descr_fields = ["AA_DESCR1", "AA_DESCR2", "MM_DESCR1", "MM_DESCR2"]


""" PARSERS """


# PARSER ARTICOLI
def art_parser(conn, giac_dict, ubic_dict, dbf_path=DBF_DIR / "ANAART.dbf", col_map=art_col_map, encoding="latin1"):
    filtered_records = filter_columns(DBF(dbf_path, encoding=encoding), col_map)

    for record in records_to_strings(filtered_records):

        # Passes raw data to the class
        new_row = {col_map[k]: record[k] for k in col_map if k in record}
        new_obj = Articolo.from_dbf_row(new_row)

        # Inserts addictional data
        lotti = giac_dict.get(new_obj.codart)
        if lotti is None:
            #print(f"Articolo {new_obj.codart} non trovato in giac_dict\n")
            lotti = {}  # per non rompere il resto del parser

        ubicazione = ubic_dict.get(new_obj.codart)
        if ubicazione is None:
            #print(f"Articolo {new_obj.codart} non trovato in ubic_dict\n")
            ubicazione = "ND"

        if len(lotti) == 1:
            tot_giacenza = sum(lotti.values())
        else:
            tot_giacenza = sum(v for k, v in lotti.items() if k != "no_lotto")
        new_obj.set_giacenza(tot_giacenza)
        new_obj.set_lotti(lotti)
        new_obj.set_ubicazione(ubicazione)

        object_to_table(conn, new_obj, "articoli")


# PARSER MOVIMENTI
def mov_parser(conn, dbf_path=DBF_DIR / "MOVMAG.dbf", col_map=mov_col_map, encoding="latin1"):
    filtered_records = filter_columns(DBF(dbf_path, encoding=encoding), col_map)

    for record in records_to_strings(filtered_records):
        # Filtra solo le righe con movimenti validi
        if (
            record.get("MM_CODART") in ("1", "2", "TRASP")
            or record.get("MM_CODCAU") not in ("ACQ", "CAR", "DDT", "GI", "SCA")
            or record.get("MM_QUANTI") == 0
        ):
            continue

        # Passes raw data to the class
        new_row = {col_map[k]: record[k] for k in col_map if k in record}
        new_obj = Movimento.from_dbf_row(new_row)
        object_to_table(conn, new_obj, "movimenti")


# PARSER CLIENTI
def clie_parser(conn, dbf_path=DBF_DIR / "SOTT.dbf", col_map=clie_col_map, encoding="latin1"):
    filtered_records = filter_columns(DBF(dbf_path, encoding=encoding), col_map)

    for record in records_to_strings(filtered_records):
        # Filtra solo i clienti (SO_ALIAS che non iniziano con F)
        if record.get("SO_ALIAS").startswith("F"):
            continue

        # Passes raw data to the class
        new_row = {col_map[k]: record[k] for k in col_map if k in record}
        new_obj = Cliente.from_dbf_row(new_row)
        object_to_table(conn, new_obj, "clienti")


#PARSER FORNITORI
def forn_parser(conn, dbf_path=DBF_DIR / "SOTT.dbf", col_map=forn_col_map, encoding="latin1"):
    filtered_records = filter_columns(DBF(dbf_path, encoding=encoding), col_map)

    for record in records_to_strings(filtered_records):
        # Filtra solo i clienti (SO_ALIAS che iniziano con F)
        if not record.get("SO_ALIAS").startswith("F"):
            continue

        # Passes raw data to the class
        new_row = {col_map[k]: record[k] for k in col_map if k in record}
        new_obj = Fornitore.from_dbf_row(new_row)
        object_to_table(conn, new_obj, "fornitori")


# PARSER LOTTI
def lotto_parser(conn, giac_dict, dbf_path=DBF_DIR / "TAGCOL.dbf", col_map=lotto_col_map, encoding="latin1"):
    filtered_records = filter_columns(DBF(dbf_path, encoding=encoding), col_map)

    for record in records_to_strings(filtered_records):
        # Passes raw data to the class
        new_row = {col_map[k]: record[k] for k in col_map if k in record}
        new_obj = Lotto.from_dbf_row(new_row)

        # Inserts addictional data
        giacenza = giac_dict.get(new_obj.codart, {}).get(new_obj.cod_lotto, 0)
        new_obj.set_giacenza(giacenza)

        object_to_table(conn, new_obj, "lotti")


""" HELPER FUNCTIONS """


# Generator function to filter the useful columns from a table returned by dbfread
def filter_columns(table, columns):
    if isinstance(columns, dict):
        cols = set(columns.keys())
    else:
        cols = set(columns)

    for record in table:
        yield {k: v for k, v in record.items() if k in cols}


# Generator function to convert the non numeric fields of a row to clean strings
def records_to_strings(filtered_records, numeric_fields=numeric_fields):
    for record in filtered_records:
        yield {
            k: (
                v if k in numeric_fields
                else str(v).strip().replace(",", ".") if k in codart_fields and v is not None
                else str(v).strip().replace("\n", " ").replace("\r", " ") if k in descr_fields and v is not None
                else str(v).strip() if v is not None
                else ""
            )
            for k, v in record.items()}


def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


# Function to create a {ARTICOLO: {LOTTO: GIACENZA}} dictionary of diactionaries,
# indicized by CODART, so the parser can immediately get the correct data for a given ARTICOLO
def calc_giac(filtered_giac):
    giac_dict = {}

    for record in filtered_giac:
        if not record.get("PM_CODART"):
            continue

        codart = record["PM_CODART"].ljust(25)
        lotto = record.get("PM_TAGCOL") or "no_lotto"
        qta_ini = safe_float(record.get("PM_QTAINI"))
        qta_acq = safe_float(record.get("PM_QTAACQ"))
        qta_car = safe_float(record.get("PM_QTACAR"))
        qta_ven = safe_float(record.get("PM_QTAVEN"))
        qta_sca = safe_float(record.get("PM_QTASCA"))

        giacenza = qta_ini + qta_acq + qta_car - qta_ven - qta_sca

        if codart not in giac_dict:
            giac_dict[codart] = {}
        giac_dict[codart][lotto] = giacenza

    return giac_dict


# Function to create a {ARTICOLO: UBICAZIONE} dictionary,
# indicized by CODART, so the parser can immediately get the correct data for a given ARTICOLO
def find_ubic(filtered_ubic):
    ubic_dict = {}
    for record in filtered_ubic:
        codart = str(record["IM_CODART"]).ljust(25)
        ubicazione = (str(record["IM_UBICAZ"]) or "").strip()

        if not ubicazione:
            continue


        if codart not in ubic_dict:
            ubic_dict[codart] = ubicazione
        elif codart in ubic_dict and str(record["IM_TAGCOL"]).strip() == "":
            ubic_dict[codart] = ubicazione

    return ubic_dict


# Function to create the auxiliary dictionaries used to set GIACENZA, LOTTO and UBICAZIONE within some of the parser functions
def create_giac_ubic_dicts(encoding="latin1"):
    filtered_giac = list(records_to_strings(filter_columns(DBF(DBF_DIR / "PROMAG.DBF", encoding=encoding), giac_fields)))
    filtered_giac.sort(key=lambda r: int(r.get("PM_ANNRIF", 0)))
    filtered_ubic = list(records_to_strings(filter_columns(DBF(DBF_DIR / "IMPEGNI.DBF", encoding=encoding), ubic_fields)))
    giac_dict = calc_giac(filtered_giac)
    ubic_dict = find_ubic(filtered_ubic)
    return giac_dict, ubic_dict


# General function to insert objects into the new database, which will be called by every parser:
def object_to_table(conn: sqlite3.Connection, obj: object, table_name: str):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    table_cols = [row[1] for row in cursor.fetchall()]

    obj_dict = {k: v for k, v in vars(obj).items() if k in table_cols}

    if not obj_dict:
        raise ValueError("L'oggetto non ha campi compatibili con la tabella")

    cols = list(obj_dict.keys())
    placeholders = ", ".join(["?"] * len(cols))
    cols_str = ", ".join(cols)
    values = list(obj_dict.values())

    sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"

    try:
        cursor.execute(sql, values)
    except sqlite3.IntegrityError as e:
        print(f"Errore di integrità saltato: {e}")
        print("Dati della riga saltata:")
        for k, v in obj_dict.items():
            print(f"  {k}: {v}")


""" MAIN """


def main():
    start = time.time()
    sys.stdout = open(DBF_DIR / "log.txt", "w", encoding="utf-8")

    conn = sqlite3.connect(DB_PATH)
    print("Connessione a DB aperta")
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        giac_dict, ubic_dict = create_giac_ubic_dicts()
        art_parser(conn, giac_dict, ubic_dict)
        print("Articoli fatti")
        lotto_parser(conn, giac_dict)
        print("Lotti fatti")
        clie_parser(conn)
        print("Clienti fatti")
        forn_parser(conn)
        print("Fornitori fatti")
        mov_parser(conn)
        print("Movimenti fatti")

    finally:
        conn.commit()
        conn.close()
        print("Connessione a DB chiusa")

    end = time.time()
    print(f"Tempo impiegato: {end - start:.2f} secondi")


if __name__ == "__main__":
    main()
