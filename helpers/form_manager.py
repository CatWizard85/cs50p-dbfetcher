FORM_MAP = {
    # Articoli fields
    "ordinamento": "text_equal",
    "codice": "text_like",
    "scelta": "num",
    "spessore": "num",
    "grammi": "num",
    "lato_a": "num",
    "lato_b": "num",
    "descrizione": "text_like",
    "giacenza": "num",
    "fsc_1": "text_equal",
    "fsc_2": "text_equal",
    "gest_lotti": "bool",
    "ubicazione": "text_equal",
    # Movimenti fields
    "codart": "text_equal",
    "tipo_mov": "text_equal",
    "tipo_doc": "text_equal",
    "record": "num",
    "num_doc": "num",
    "data": "date",
    # Lotti fields
    "cod_lotto": "text_like",
    # Clienti/Fornitori fields
    "cod_clie": "text_equal",
    "cod_forn": "text_equal",
    "nome": "text_like",
}


def clean_form(fd):
    clean_fd = {}

    for field in fd:

        if field == "codart":
            clean_fd[field] = fd.get(field)
            continue

        base = field.replace("_min", "").replace("_max", "")
        if base not in FORM_MAP:
            print(f"WARNING: {field} not in FORM_MAP!")
            continue

        ftype = FORM_MAP[base]
        value = fd.get(field, "")

        if ftype.startswith("text") or ftype == "date":
            value = value.strip().lower()
            clean_fd[field] = value or None

        elif ftype == "num":
            value = value.strip().replace(",", ".")
            try:
                clean_fd[field] = float(value)
            except (ValueError, AttributeError):
                clean_fd[field] = None

        elif ftype == "bool":
            if value == "1":
                clean_fd[field] = 1
            elif value == "0":
                clean_fd[field] = 0
            else:
                clean_fd[field] = None


    return clean_fd
