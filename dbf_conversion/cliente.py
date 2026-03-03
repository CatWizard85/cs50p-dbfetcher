from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class Cliente:
    cod_clie: str # rif SO_ALIAS
    nome: str # rif SO_DESSOT
    indirizzo: str
    citta: str
    provincia: str
    num_tel: str
    note: Optional[str] = None


    @staticmethod
    def from_dbf_row(row: dict) -> "Cliente":

        try:
            clean_row = {}

            clean_row["cod_clie"] = row.get("cod_clie")
            clean_row["nome"] = row.get("nome")
            clean_row["indirizzo"] = row.get("indirizzo")
            clean_row["citta"] = row.get("citta")
            clean_row["provincia"] = row.get("provincia")
            clean_row["num_tel"] = row.get("num_tel")

            return Cliente(**clean_row)

        except Exception as e:
            raise RuntimeError(f"Errore nella conversione dei clienti: {e}\nRiga problematica: {row}")
