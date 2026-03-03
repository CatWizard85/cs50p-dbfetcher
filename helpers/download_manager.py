from io import BytesIO
from flask import send_file
import pandas as pd

HEADERS_MAP = {
    "id": "ID",
    "codice": "Codice",
    "scelta": "Scelta",
    "spessore": "Spessore",
    "grammi": "Grammi",
    "lato_a": "Lato A",
    "lato_b": "Lato B",
    "descrizione": "Descrizione",
    "um": "UM",
    "giacenza": "Giacenza",
    "fsc_1": "Cat. FSC 1",
    "fsc_2": "Cat. FSC 2",
    "gest_lotti": "Gest. Lotti",
    "ubicazione": "Ubicazione",
    "codart": "Codice Articolo",
    "tipo_mov": "Tipo Movimento",
    "tipo_doc": "Tipo Documento",
    "record": "Record",
    "num_doc": "Numero Documento",
    "data": "Data",
    "quantita": "Quantita",
    "prezzo": "Prezzo",
    "cod_lotto": "Lotto",
    "cod_clie": "Codice Cliente",
    "cod_forn": "Codice Fornitore",
    "nome": "Ragione Sociale",
    "indirizzo": "Indirizzo",
    "citta": "Citta",
    "provincia": "Provincia",
    "num_tel": "Telefono",
    "nome_clie": "Rag. Soc. Cliente",
    "nome_forn": "Rag. Soc. Fornitore",
    "note": "Note",
}


def create_excel(results, search_function_name, is_lista=False):

    df = pd.DataFrame(results)

    if is_lista:
        df.drop(columns=[HEADERS_MAP.get("codart"), HEADERS_MAP.get("scelta")], inplace=True)
        col_index = df.columns.get_loc(HEADERS_MAP.get("lato_b"))
        df.insert(col_index, "x", "x")
        col_index = df.columns.get_loc(HEADERS_MAP.get("prezzo"))
        df.insert(col_index, "Fogli", df["Giacenza"]/(df["Grammi"]*df["Lato A"]*df["Lato B"])*10000000)
        df["Fogli"] = df["Fogli"].fillna(0).round(0)
        df = df.sort_values(by=["Spessore", "Grammi", "Codice"], ascending=True)
        df = df.reset_index(drop=True)

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"{search_function_name}.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
