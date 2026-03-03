from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class Lotto:
    codart: str # rif TC_CODART
    cod_lotto: str # rif TC_TAGCOL
    giacenza: float = 0 # rif DERIVATO
    note: Optional[str] = None


    @staticmethod
    def from_dbf_row(row: dict) -> "Lotto":

        try:

            clean_row = {}
            codart = row.get("codart").ljust(25)

            clean_row["codart"] = codart
            clean_row["cod_lotto"] = row.get("cod_lotto")

            return Lotto(**clean_row)

        except Exception as e:
            raise RuntimeError(f"Errore nella conversione dei lotti: {e}\nRiga problematica: {row}")


    def set_giacenza(self, giacenza: float):
        self.giacenza = giacenza or 0.0
