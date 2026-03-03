from .form_manager import FORM_MAP


# Funzione che prende form_data, ci itera sopra, confronta i campi con la mappa FORM_MAP, costruisce le condizioni per la query, restituisce condizioni e parametri
def build_conditions(fd, is_mov=False):
    conditions = []
    params = []
    order_condition = False
    order_param = None

    for field in fd:

        if field.endswith("_min") or field.endswith("_max"):
            continue

        if field == "ordinamento":
            order_condition = True
            order_param = fd.get(field)
            continue

        ftype = FORM_MAP[field]
        value = fd.get(field, "")

        if ftype == "text_equal" and value:
            prefix = "movimenti." if is_mov and field in ("cod_forn", "cod_clie") else ""  # This is for the mov_search because it joins two tables
            conditions.append(f"{prefix}{field} = ? COLLATE NOCASE")
            params.append(value)

        elif ftype == "text_like" and value:
            conditions.append(f"{field} LIKE ? COLLATE NOCASE")
            params.append(f"%{value}%")

        elif ftype == "bool" and value is not None:
            conditions.append(f"{field} = ?")
            params.append(value)

        elif ftype == "num" or ftype == "date":
            value_min = fd.get(field+"_min")
            value_max = fd.get(field+"_max")

            range_condition, range_params = add_range(field, value, value_min, value_max)
            if range_condition:
                conditions.append(range_condition)
                params.extend(range_params)

    return conditions, params, order_condition, order_param


def add_range(field, value, value_min, value_max):
    range_condition = None
    range_params = () # This must be iterable for the db.execute function

    if value is not None:
        range_condition = f"{field} = ?"
        range_params = (value,)

    elif value_min is not None and value_max is not None:
        range_condition = f"{field} BETWEEN ? AND ?"
        range_params = (value_min, value_max)

    elif value_min is not None:
        range_condition = f"{field} >= ?"
        range_params = (value_min,)

    elif value_max is not None:
        range_condition = f"{field} <= ?"
        range_params = (value_max,)

    return range_condition, range_params
