from datetime import date
from io import BytesIO
from flask import send_file
import pandas as pd
import sys

COLUMNS = ["MESE", "VEN_TOT_PESI", "VEN_TOT_IMPONIBILE", "VEN_PREZZO_MEDIO", "", "MESE", "ACQ_TOT_PESI", "ACQ_TOT_IMPONIBILE", "ACQ_PREZZO_MEDIO"]
MESI_MAP = {
    1: "GENNAIO",
    2: "FEBBRAIO",
    3: "MARZO",
    4: "APRILE",
    5: "MAGGIO",
    6: "GIUGNO",
    7: "LUGLIO",
    8: "AGOSTO",
    9: "SETTEMBRE",
    10: "OTTOBRE",
    11: "NOVEMBRE",
    12: "DICEMBRE"
}


def create_dict_mesi(lista, year=2025):
    mesi = {i: 0 for i in range(1, 13)}
    mesi = {i: {"tot_quant": 0, "tot_val": 0, "prezzi": []} for i in range(1, 13)}

    for row in lista:
        row_record = row.get("record")

        try:
            cur_date = date.fromisoformat(row.get("data"))
        except ValueError:
            print(f"Il record {row_record} ha data non valida")
            continue

        cur_year = cur_date.year
        if cur_year != year:
            continue

        row_quant = row.get("quantita")
        if row_quant is None:
            print(f"Il record {row_record} non ha quantita")
            continue

        row_um = row.get("um")
        if not row_um:
            continue
        if row_um not in ("KG", "kg", "Kg", "kG"):
            continue

        row_prezzo = row.get("prezzo")
        if not row_prezzo:
            print(f"Il record {row_record} non ha prezzo")

        cur_mon = cur_date.month

        mesi[cur_mon]["tot_quant"] += row_quant
        mesi[cur_mon]["tot_val"] += row_quant * row_prezzo
        mesi[cur_mon]["prezzi"].append(row_prezzo)

    for mese in mesi:
        mesi[mese]["tot_quant"] = round((mesi[mese]["tot_quant"] / 100), 2)
        mesi[mese]["tot_val"] = round(mesi[mese]["tot_val"], 2)
        prezzi = mesi[mese]["prezzi"]
        mesi[mese]["prezzo_m"] = round((sum(prezzi)/len(prezzi) if prezzi else 0), 3)

    return mesi


def create_excel_entrate_uscite(lista_entrate, lista_uscite):
    sys.stdout = open("log_entrate_uscite.txt", "w", encoding="utf-8")
    print("LOG CREAZIONE FILE ENTRATE/USCITE")

    dict_entrate = create_dict_mesi(lista_entrate)
    dict_uscite = create_dict_mesi(lista_uscite)

    df_entrate = pd.DataFrame.from_dict(dict_entrate, orient="index")
    df_uscite = pd.DataFrame.from_dict(dict_uscite, orient="index")

    df = pd.concat([df_uscite, df_entrate], axis=1)
    df.insert(len(df_entrate.columns), "E_MESE", list(MESI_MAP.values()))
    df.insert(len(df_entrate.columns), "-", "")
    df.insert(0, "U_MESE", list(MESI_MAP.values()))
    df = df.drop(columns=["prezzi"], errors="ignore")
    df.columns = COLUMNS

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="entrate_uscite.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
