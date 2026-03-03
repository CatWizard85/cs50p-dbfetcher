from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class Movimento:
    record: int # rif MM_RECORD
    tipo_mov: str # 'carico', 'scarico' - rif DERIVATO
    data: str # rif MM_DATDOC
    tipo_doc: str # 'ddt_carico', 'ddt_scarico', 'fatt_carico', 'fatt_scarico', 'interno_carico', 'interno_scarico' - rif MM_CODCAU
    num_doc: Optional[int] = None # rif MM_NUMDOC
    cod_forn: Optional[str] = None # rif MM_ALIAS
    cod_clie: Optional[str] = None # rif MM_ALIAS
    codart: Optional[str] = None # rif MM_CODART
    cod_lotto: Optional[str] = None # rif MM_TAGCOL
    descrizione: Optional[str] = None # rif MM_DESCR1 e MM_DESCR2 unite
    um: str = "kg" # rif MM_UNIMIS
    quantita: float = 0 # rif MM_QUANTI
    prezzo: float = 0 # rif MM_PREZZO
    note: Optional[str] = None

    CAUSALI_CARICO = ("GI", "ACQ", "CAR")
    TIPO_DOC_MAP = {
        "GI": "giac_iniziale",
        "ACQ": "ddt_carico",
        "CAR": "int_carico",
        "DDT": "ddt_scarico",
        "SCA": "int_scarico",
    }


    @staticmethod
    def from_dbf_row(row: dict) -> "Movimento":

        try:
            clean_row = {}

            if (cod := row.get("record")):
                clean_row["record"] = int(cod)
            else:
                clean_row["record"] = 0
            clean_row["tipo_mov"] = "carico" if row.get("tipo_doc") in Movimento.CAUSALI_CARICO else "scarico"
            clean_row["data"] = row.get("data")
            clean_row["tipo_doc"] = Movimento.TIPO_DOC_MAP.get(row.get("tipo_doc"), "ND")
            if (cod := row.get("num_doc")):
                clean_row["num_doc"] = int(cod)
            else:
                clean_row["num_doc"] = 0
            if (cod := row.get("cod_clifor")):
                if cod.startswith("F"):
                    clean_row["cod_forn"] = cod
                else:
                    clean_row["cod_clie"] = cod
            if (cod := row.get("codart")):
                clean_row["codart"] = cod.ljust(25)
            clean_row["cod_lotto"] = row.get("cod_lotto")
            clean_row["descrizione"] = ((row.get("descr1") or "") + " " + (row.get("descr2") or "")).strip()
            clean_row["um"] = row.get("um")
            clean_row["quantita"] = float(row.get("quantita"))
            clean_row["prezzo"] = float(row.get("prezzo"))

            return Movimento(**clean_row)

        except Exception as e:
            raise RuntimeError(f"Errore nella conversione dei movimenti: {e}\nRiga problematica: {row}")
