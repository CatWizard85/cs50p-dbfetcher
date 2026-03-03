from dataclasses import dataclass, field
from typing import Optional

@dataclass(kw_only=True)
class Articolo:
    codart: str  # Codice completo ottenuto dai sottocampi? O da AA_CODART?
    codice: str
    spessore: Optional[float] = None
    scelta: Optional[int] = None
    grammi: Optional[int] = None
    lato_a: Optional[float] = None
    lato_b: Optional[float] = None
    descrizione: Optional[str] = None # rif AA_DESCR1 e AA_DESCR2 unite
    um: str = "kg" # rif AA_UNIMIS
    giacenza: float = 0 # rif tabella PROMAG
    fsc_1: Optional[str] = None # rif AA_USER2
    fsc_2: Optional[str] = None # rif AA_USER3
    ubicazione: Optional[str] = None # rif tabella IMPEGNI??
    gest_lotti: bool = False
    note: Optional[str] = None

    lotti: dict[str, float] = field(default_factory=dict)


    @staticmethod
    def from_dbf_row(row: dict) -> "Articolo":

        try:

            clean_row = {}
            codart = row.get("codart").ljust(25)

            clean_row["codart"] = codart
            clean_row["codice"] = codart[:5].strip()
            clean_row["spessore"] = Articolo.safe_type_convert(codart[5:9], float)
            clean_row["scelta"] = Articolo.safe_type_convert(codart[9:11], int)
            clean_row["grammi"] = 1000 if codart[11:15].strip() == "1OOO" else Articolo.safe_type_convert(codart[11:15], int)
            clean_row["lato_a"] = Articolo.safe_type_convert(codart[15:20], float)
            clean_row["lato_b"] = Articolo.safe_type_convert(codart[20:], float)
            clean_row["descrizione"] = ((row.get("descr1") or "") + " " + (row.get("descr2") or "")).strip()
            clean_row["um"] = row.get("um")
            if (cod := row.get("fsc_1")):
                clean_row["fsc_1"] = cod
                clean_row["gest_lotti"] = True
            if (cod := row.get("fsc_2")):
                clean_row["fsc_2"] = cod

            return Articolo(**clean_row)

        except Exception as e:
            raise RuntimeError(f"Errore nella conversione degli articoli: {e}\nRiga problematica: {row}")


    # Function to convert substrings in numeric types avoiding errors when the string is empty
    @staticmethod
    def safe_type_convert(s, typ, default=None):
        try:
            s = s.strip()
            return typ(s)
        except (ValueError, TypeError):
            return default


    def set_giacenza(self, giacenza: float):
        self.giacenza = giacenza or 0.0


    def set_lotti(self, lotti: dict[str, float]):
        self.lotti = lotti


    def set_ubicazione(self, ubicazione: str):
        self.ubicazione = ubicazione or "ND"
